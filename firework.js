<<<<<<< HEAD
const canvas = document.getElementById("fireworksCanvas");
const ctx = canvas.getContext("2d");
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

class Firework {
    constructor(x, y, color) {
        this.x = x;
        this.y = y;
        this.color = color;
        this.particles = [];

        for (let i = 0; i < 30; i++) {
            this.particles.push({
                x: x,
                y: y,
                speed: Math.random() * 3 + 2,
                angle: Math.random() * Math.PI * 2,
                radius: Math.random() * 4 + 2,
                alpha: 1,
                decay: Math.random() * 0.02 + 0.01,
            });
        }
    }

    update() {
        this.particles.forEach((p, index) => {
            p.x += Math.cos(p.angle) * p.speed;
            p.y += Math.sin(p.angle) * p.speed;
            p.alpha -= p.decay;
            if (p.alpha <= 0) {
                this.particles.splice(index, 1);
            }
        });
    }

    draw() {
        this.particles.forEach((p) => {
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
            ctx.fillStyle = `rgba(${this.color}, ${p.alpha})`;
            ctx.fill();
        });
    }
}

const fireworks = [];
function launchFirework() {
    const x = Math.random() * canvas.width;
    const y = Math.random() * (canvas.height / 2);
    const colors = ["255,0,0", "0,255,0", "0,0,255", "255,255,0", "255,0,255"];
    const color = colors[Math.floor(Math.random() * colors.length)];

    fireworks.push(new Firework(x, y, color));
}

function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    fireworks.forEach((firework, index) => {
        firework.update();
        firework.draw();
        if (firework.particles.length === 0) {
            fireworks.splice(index, 1);
        }
    });
    requestAnimationFrame(animate);
}

setInterval(launchFirework, 700); // Launch a new firework every 0.7s
animate();

// Stop fireworks after 7 seconds
setTimeout(() => {
    clearInterval(launchFirework);
}, 7000);
=======
const canvas = document.getElementById("fireworksCanvas");
const ctx = canvas.getContext("2d");
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

class Firework {
    constructor(x, y, color) {
        this.x = x;
        this.y = y;
        this.color = color;
        this.particles = [];

        for (let i = 0; i < 30; i++) {
            this.particles.push({
                x: x,
                y: y,
                speed: Math.random() * 3 + 2,
                angle: Math.random() * Math.PI * 2,
                radius: Math.random() * 4 + 2,
                alpha: 1,
                decay: Math.random() * 0.02 + 0.01,
            });
        }
    }

    update() {
        this.particles.forEach((p, index) => {
            p.x += Math.cos(p.angle) * p.speed;
            p.y += Math.sin(p.angle) * p.speed;
            p.alpha -= p.decay;
            if (p.alpha <= 0) {
                this.particles.splice(index, 1);
            }
        });
    }

    draw() {
        this.particles.forEach((p) => {
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
            ctx.fillStyle = `rgba(${this.color}, ${p.alpha})`;
            ctx.fill();
        });
    }
}

const fireworks = [];
function launchFirework() {
    const x = Math.random() * canvas.width;
    const y = Math.random() * (canvas.height / 2);
    const colors = ["255,0,0", "0,255,0", "0,0,255", "255,255,0", "255,0,255"];
    const color = colors[Math.floor(Math.random() * colors.length)];

    fireworks.push(new Firework(x, y, color));
}

function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    fireworks.forEach((firework, index) => {
        firework.update();
        firework.draw();
        if (firework.particles.length === 0) {
            fireworks.splice(index, 1);
        }
    });
    requestAnimationFrame(animate);
}

setInterval(launchFirework, 700); // Launch a new firework every 0.7s
animate();

// Stop fireworks after 7 seconds
setTimeout(() => {
    clearInterval(launchFirework);
}, 7000);
>>>>>>> 428c8bdaee0fdf276b8897c3c7eae19a60144c26
