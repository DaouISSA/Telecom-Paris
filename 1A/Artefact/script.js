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
