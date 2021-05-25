function Calculate(){
    let w = document.getElementById('weight').value;
    let h = document.getElementById('height').value;
    let a = document.getElementById('age').value;

    if (document.getElementById('male').checked){
        var ree = (10 * w + 6.25 * h - 5 * a + 5);
    } else if (document.getElementById('female').checked){
        var ree = (10 * w + 6.25 * h - 5 * a + 161);
    }
    let s = document.getElementById('activity').value;
    if (s == 'Sedentary') {
        var tdee = ree * 1.2;
    }
    else if (s == 'Light - 3 times per week') {
        var tdee = ree * 1.375;
    }
    else if (s == 'Mid - 5 times per week') {
        var tdee = ree * 1.55;
    }
    else {
        var tdee = ree * 1.725;
    }

    document.getElementById('results').innerHTML = tdee + ' kcal per day';

}
