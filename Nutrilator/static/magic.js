function Calculate(){
    let w = document.getElementById('weight').value;
    let h = document.getElementById('height').value;
    let a = document.getElementById('age').value;
    let g = document.getElementById('goal').value;
    var html = '';

    // Check for completion of required fields
    if (!w || !h || !a || !g){
        return document.getElementById('results').innerHTML = 'Make sure all fields are completed!';
    }

    // Check gender for calculation
    if (document.getElementById('male').checked){
        var ree = (10 * w + 6.25 * h - 5 * a + 5);
    } else if (document.getElementById('female').checked){
        var ree = (10 * w + 6.25 * h - 5 * a - 161);
    }

    // Retrieve act level
    let s = document.getElementById('activity').value;

    // Perform calculation of kcal/day
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

    // Check goal
    if (g == 'Lose weight') {
        tdee = tdee - (tdee * 0.20);
    }
    else if (g == 'Gain weight') {
        tdee = tdee + (tdee * 0.20);
    }

    // Calculate macros
    let protein = 0.825 * (w/0.453592);
    let fat = (tdee * 0.3) / 9;
    let carbo = (tdee - (protein * 4) - (fat * 9)) / 4

    // Assign to html var
    html += tdee + ' kcal per day' + '<br/>';
    html += protein + ' g of protein per day' + '<br/>';
    html += fat + ' g of fat per day' + '<br/>';
    html += carbo + ' g of carbos per day' + '<br/>';

    return document.getElementById('results').innerHTML = html;
}
