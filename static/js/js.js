document.addEventListener('DOMContentLoaded', function() {
    const svg = document.getElementById('hearts');
    const width = window.innerWidth;
    const height = window.innerHeight;

    for (let i = 0; i < 50; i++) {
        const use = document.createElementNS('http://www.w3.org/2000/svg', 'use');
        use.setAttributeNS('http://www.w3.org/1999/xlink', 'xlink:href', '#heart');
        use.setAttribute('x', Math.random() * width - 600);
        use.setAttribute('y', Math.random() * height - 400);
        use.setAttribute('width', Math.random() * 50 + 10);
        use.setAttribute('height', Math.random() * 50 + 10);
        use.style.animation = `float ${Math.random() * 10 + 5}s ease-in-out infinite`;
        svg.appendChild(use);
    }

    const style = document.createElement('style');
    style.innerHTML = `
        @keyframes float {
            0% { transform: translateY(0) }
            50% { transform: translateY(-20px) }
            100% { transform: translateY(0) }
        }
    `;
    document.head.appendChild(style);
});
