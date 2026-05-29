let joystick = document.getElementById("joystick");
let joystickZone = document.getElementById("joystickZone");

let maxDistance = 100; // Distance maximale de déplacement du joystick (px)
let centerX = joystickZone.offsetWidth / 2;
let centerY = joystickZone.offsetHeight / 2;

// Position initiale du joystick
joystick.style.left = centerX + 'px';
joystick.style.top = centerY + 'px';

joystickZone.addEventListener('touchmove', function (event) {
    let touch = event.touches[0];
    let x = touch.pageX - joystickZone.offsetLeft - centerX;
    let y = touch.pageY - joystickZone.offsetTop - centerY;

    let distance = Math.sqrt(x * x + y * y);
    if (distance > maxDistance) {
        x = x / distance * maxDistance;
        y = y / distance * maxDistance;
    }

    joystick.style.left = (centerX + x) + 'px';
    joystick.style.top = (centerY + y) + 'px';

    let normalizedX = x / maxDistance;  // Normalisation de l'axe X entre -1 et 1
    let normalizedY = -y / maxDistance;  // Inversion de Y pour que le haut soit positif

    // Envoie les valeurs des roues en fonction du joystick
    sendWheelSpeeds(normalizedX, normalizedY);
}, false);

joystickZone.addEventListener('touchend', function () {
    // Recentrer le joystick lorsque l'utilisateur lâche
    joystick.style.left = centerX + 'px';
    joystick.style.top = centerY + 'px';
    sendWheelSpeeds(0, 0);  // Stop le robot quand on relâche
}, false);

function sendWheelSpeeds(x, y) {
    // Calcul des vitesses pour chaque roue en fonction du joystick
    let maxSpeed = 120;  // Vitesse maximale des roues
    let leftSpeed = y + x;  // Vitesse de la roue gauche
    let rightSpeed = y - x;  // Vitesse de la roue droite

    // Limiter la vitesse entre -maxSpeed et maxSpeed
    leftSpeed = Math.max(-maxSpeed, Math.min(maxSpeed, leftSpeed * maxSpeed));
    rightSpeed = Math.max(-maxSpeed, Math.min(maxSpeed, rightSpeed * maxSpeed));

    // Envoie les commandes des roues au serveur
    fetch('/control_motor_wheel', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            left: Math.round(leftSpeed),  // Arrondi la vitesse pour l'envoi
            right: Math.round(rightSpeed)
        })
    })
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.log('Erreur', error));
}
function switchMode() {
    var modeBoutons = document.getElementById("modeBoutons");
    var modeBarres = document.getElementById("modeBarres");
    var modeSwitch = document.getElementById("modeSwitch");

    if (modeBoutons.style.display === "none") {
        modeBoutons.style.display = "block";
        modeBarres.style.display = "none";
        modeSwitch.value = "Passer en mode Barres";
    } else {
        modeBoutons.style.display = "none";
        modeBarres.style.display = "block";
        modeSwitch.value = "Passer en mode Boutons";
    }
}

var intervalGauche, intervalDroite, intervalSend, old_value_left, old_value_right;
intervalSend = setInterval(sendData, 100);
function fct_BarreGauche() {
    var barreGauche = document.getElementById("barreGauche");
    clearInterval(intervalGauche);
    barreGauche.onmouseup = barreGauche.ontouchend = function () {
        intervalGauche = setInterval(function () {
            if (barreGauche.value > 0) {
                barreGauche.value--;
            } else if (barreGauche.value < 0) {
                barreGauche.value++;
            }
            if (barreGauche.value == 0) {
                clearInterval(intervalGauche);
            }
        }, 15);
    };
}

function fct_BarreDroite() {
    var barreDroite = document.getElementById("barreDroite");
    clearInterval(intervalDroite);
    barreDroite.onmouseup = barreDroite.ontouchend = function () {
        intervalDroite = setInterval(function () {
            if (barreDroite.value > 0) {
                barreDroite.value--;
            } else if (barreDroite.value < 0) {
                barreDroite.value++;
            }
            if (barreDroite.value == 0) {
                clearInterval(intervalDroite);
            }
        }, 15);
    };
}

function sendData() {
    var value_left = document.getElementById("barreGauche").value;
    var value_right = document.getElementById("barreDroite").value;

    if (old_value_left != value_left || old_value_right != value_right) {
        fetch('/control_motor_wheel', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                left: value_left,
                right: value_right
            })
        })
        .then(response => response.json())
        .then(data => console.log(data))
        .catch(error => console.log('Erreur', error));
    }
    old_value_left = value_left;
        old_value_right = value_right;
}
function fct_go_to_case(x, y) {
    fetch('/go_to_case', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            case_x: x,
            case_y: y
        })
    })
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.log('Erreur', error));
}
function fct_Stop() {
    fetch('/control_motor', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            forward: 0,
            backward: 0,
            right: 0,
            left: 0
        })
    })
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.log('Erreur', error));
}
function fct_Avancer() {
    fetch('/control_motor', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            forward: 1,
            backward: 0,
            right: 0,
            left: 0
        })
    })
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.log('Erreur', error));
}

function fct_Reculer() {
    fetch('/control_motor', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            forward: 0,
            backward: 1,
            right: 0,
            left: 0
        })
    })
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.log('Erreur', error));
}

function fct_Droite() {
    fetch('/control_motor', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            forward: 0,
            backward: 0,
            right: 1,
            left: 0
        })
    })
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.log('Erreur', error));
}

function fct_Gauche() {
    fetch('/control_motor', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            forward: 0,
            backward: 0,
            right: 0,
            left: 1
        })
    })
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.log('Erreur', error));
}