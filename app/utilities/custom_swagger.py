html = """
    <!DOCTYPE html>
    <html>
    <head>
        <link type="text/css" rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css">
        <link rel="shortcut icon" href="https://fastapi.tiangolo.com/img/favicon.png">
        <title>RevCare API</title>
    </head>
    <body>
        <div id="swagger-ui"></div>
        <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js"></script>

        <script>
        const ui = SwaggerUIBundle({
            url: '/openapi.json',
            dom_id: '#swagger-ui',
            layout: 'BaseLayout',
            deepLinking: true,
            showExtensions: true,
            showCommonExtensions: true,
            presets: [
                SwaggerUIBundle.presets.apis,
                SwaggerUIBundle.SwaggerUIStandalonePreset
            ],
            onComplete: () => {
                // Wait for DOM to be ready
                const authButton = document.querySelector('.btn.authorize.unlocked');

  
    
    // Wait a short time in case the modal content loads dynamically
    setInterval(() => {
      
      const modal = document.querySelector('.modal-ux'); // or use your modal selector
modal.querySelectorAll('*').forEach(el => {
  el.childNodes.forEach(node => {
    if (node.nodeType === 3) {
      const text = node.textContent.trim();
      if (text.includes('username')) {
        node.textContent = text.replace(/username/gi, 'phone');
      }
    }  
  });
});
    }, 1000);
            }
        });
        </script>
    </body>
    </html>
    """