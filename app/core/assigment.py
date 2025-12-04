from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Mechanic, Service, BookedService, BookingAssignment, Status

# helpers
def minmax_invert(v, min_v, max_v):
    if max_v == min_v:
        return 1.0
    return 1 - (v - min_v) / (max_v - min_v)

async def calculate_mechanic_availability(db: AsyncSession, mech: Mechanic):
    # Fetch their current assignments to estimate availability
    assignment_query = (
        select(BookingAssignment)
        .join(Status, BookingAssignment.status_id == Status.id)
        .where(
            and_(
                BookingAssignment.mechanic_id == mech.id,
                Status.name == "assigned"
            )
        )
    )
    res = await db.execute(assignment_query)
    assignments = res.scalars().all()

    availability_in_hours = 0
    for assignment in assignments:
        if assignment.assignment_type.name == 'analysis':
            # For analysis, assume fixed time
            availability_in_hours += 1
        elif assignment.assignment_type.name in ['pickup', 'drop']:
            # For pickup/drop, assume fixed time, in future it can be scaled to dynamic time
            availability_in_hours += 2
        else:
            # For service assignments, sum up remaining time of booked services
            bs_query = (
                select(BookedService, Service)
                .join(Service, BookedService.service_id == Service.id)
                .join(Status, BookedService.status_id == Status.id)
                .where(
                    and_(
                        BookedService.booking_id == assignment.booking_id,
                        Status.name == 'confirmed',
                        BookedService.completed.is_(False)
                    )
                )
            )
            bs_res = await db.execute(bs_query)
            booked_services = bs_res.all()
            for bs, svc in booked_services:
                availability_in_hours += float(svc.time_hrs)

    return availability_in_hours
    
async def get_services_to_complete(db: AsyncSession, booking_id: int):
    query = (
        select(Service)
        .join(BookedService, BookedService.service_id == Service.id)
        .join(Status, BookedService.status_id == Status.id)
        .where(
            and_(
                BookedService.booking_id == booking_id,
                Status.name == 'confirmed',
                BookedService.completed.is_(False)
            )
        )
    )
    result = await db.execute(query)
    return result.scalars().all()

def set_scores(score_obj, total, avail, skill, workload):
    score_obj['total'] = total
    score_obj['avail'] = avail
    score_obj['skill'] = skill
    score_obj['workload'] = workload

# algorithms
async def select_mechanic_for_service(db: AsyncSession, booking_id: int):
    # Fetch services in this booking that are confirmed and not completed
    services_to_complete = await get_services_to_complete(db, booking_id)
    if not services_to_complete:
        return None

    req_categories = set()
    for svc in services_to_complete:
        req_categories.add(svc.category_id)


    # Get mechanics
    result = await db.execute(select(Mechanic))
    candidates = result.scalars().all()

    # feature extraction
    availability_map = {}
    min_availability = float('inf')
    max_availability = 0

    work_load_map = {}
    min_workload = float('inf')
    max_workload = 0

    skill_scores = {}

    for mech in candidates:
        # Feature 1: Availability (in hours)
        if mech.assigned:
            availability_in_hours = await calculate_mechanic_availability(db, mech)

        else:
            availability_in_hours = 0  # Available now

        availability_map[mech.id] = availability_in_hours

        min_availability = min(min_availability, availability_in_hours)
        max_availability = max(max_availability, availability_in_hours)

        # Feature 2: Workload (mechanic score given based on difficulty handled historically)
        work_load_map[mech.id] = mech.score
        min_workload = min(min_workload, mech.score)
        max_workload = max(max_workload, mech.score)

        # Feature 3: Skill Match
        mechanic_service_categories = set()
        for category in mech.service_categories:
            mechanic_service_categories.add(category.id)

        match = len(req_categories.intersection(mechanic_service_categories))
        total = len(req_categories)
        
        skill_scores[mech.id] = match / total

    availability_scores = {
        mech_id: minmax_invert(v, min_availability, max_availability)
        for mech_id, v in availability_map.items()
    }
    workload_scores = {
        mech_id: minmax_invert(v, min_workload, max_workload)
        for mech_id, v in work_load_map.items()
    }

    best_scores = {
        'total': 0,
        'avail': 0,
        'skill': 0, 
        'workload': 0
    }
    best_mechanic = None
    for mech in candidates:
        # 1. Availability Score (Weight: 50)
        availability_score = availability_scores[mech.id]
        
        # 2. Skill Match Score (Weight: 25)
        skill_score = skill_scores[mech.id]

        # 3. Workload Score (Weight: 25)
        workload_score = workload_scores[mech.id]

        total_score = (0.5 * availability_score) + (0.25 * skill_score) + (0.25 * workload_score)

        print(f"Mechanic {mech.id} - Total Score: {total_score:.4f} (Avail: {availability_score:.4f}, Skill: {skill_score:.4f}, Workload: {workload_score:.4f})")
        
        if total_score > best_scores['total']:
            set_scores(best_scores, total_score, availability_score, skill_score, workload_score)
            best_mechanic = mech
        
        elif total_score == best_scores['total']:
            # Tie-breaker: Prefer higher skill score
            if skill_score > best_scores['skill']:
                set_scores(best_scores, total_score, availability_score, skill_score, workload_score)
                best_mechanic = mech
            
            elif skill_score == best_scores['skill']:
                # Further tie-breaker: Prefer lower availability (more available)
                if availability_score > best_scores['avail']:
                    set_scores(best_scores, total_score, availability_score, skill_score, workload_score)
                    best_mechanic = mech
                
                elif availability_score == best_scores['avail']:
                    # Final tie-breaker: Prefer lower workload
                    if workload_score > best_scores['workload']:
                        set_scores(best_scores, total_score, availability_score, skill_score, workload_score)
                        best_mechanic = mech
                        
    print(f'Best Mechanic: {best_mechanic.id if best_mechanic else None} with Scores: {best_scores}')
    return best_mechanic



async def select_mechanic_for_pickup_drop_analysis(db: AsyncSession, booking_id: int, analysis: bool):
    # Get mechanics
    base_query = select(Mechanic)

    if analysis:
        # no extra filter, consider all mechanics
        mech_query = base_query.where(Mechanic.analysis.is_(True))        
    else:
        mech_query = base_query.where(Mechanic.pickup_drop.is_(True))

    # Execute and load candidates
    result = await db.execute(mech_query)
    candidates = result.scalars().all()
    

    # feature extraction
    availability_map = {}
    min_availability = float('inf')
    max_availability = 0

    work_load_map = {}
    min_workload = float('inf')
    max_workload = 0

    for mech in candidates:
        # Feature 1: Availability (in hours)
        if mech.assigned:
            availability_in_hours = await calculate_mechanic_availability(db, mech)

        else:
            availability_in_hours = 0  # Available now

        availability_map[mech.id] = availability_in_hours

        min_availability = min(min_availability, availability_in_hours)
        max_availability = max(max_availability, availability_in_hours)

        # Feature 2: Workload (mechanic score given based on difficulty handled historically)
        work_load_map[mech.id] = mech.score
        min_workload = min(min_workload, mech.score)
        max_workload = max(max_workload, mech.score)

    availability_scores = {
        mech_id: minmax_invert(v, min_availability, max_availability)
        for mech_id, v in availability_map.items()
    }
    workload_scores = {
        mech_id: minmax_invert(v, min_workload, max_workload)
        for mech_id, v in work_load_map.items()
    }

    best_scores = {
        'total': 0,
        'avail': 0,
        'skill': 0,    # dummy
        'workload': 0
    }
    best_mechanic = None
    for mech in candidates:
        # 1. Availability Score (Weight: 70)
        availability_score = availability_scores[mech.id]

        # 2. Workload Score (Weight: 30)
        workload_score = workload_scores[mech.id]

        total_score = (0.7 * availability_score) + (0.3 * workload_score)

        print(f"Mechanic {mech.id} - Total Score: {total_score:.4f} (Avail: {availability_score:.4f}, Workload: {workload_score:.4f})")
        
        if total_score > best_scores['total']:
            set_scores(best_scores, total_score, availability_score, 0, workload_score)
            best_mechanic = mech
        
        elif total_score == best_scores['total']:
            # Tie-breaker
            if availability_score > best_scores['avail']:
                set_scores(best_scores, total_score, availability_score, 0, workload_score)
                best_mechanic = mech
            
            elif availability_score == best_scores['avail']:
                # Final tie-breaker: Prefer lower workload
                if workload_score > best_scores['workload']:
                    set_scores(best_scores, total_score, availability_score, 0, workload_score)
                    best_mechanic = mech
                        
    print(f'Best Mechanic: {best_mechanic.id if best_mechanic else None} with Scores: {best_scores}')
    return best_mechanic
