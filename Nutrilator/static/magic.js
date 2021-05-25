function Calculate(){
    if (document.getElementById('male').checked){
        var ree = (
        10 * document.getElementById('weight') + 6.25 * document.getElementById('height') - 5 * document.getElementById('age') + 5
        );
    } else if (document.getElementById('female').checked){
        var ree = (
        10 * document.getElementById('weight') +
        6.25 * document.getElementById('height') -
        5 * document.getElementById('age') -
        161
        );
    }

    if (document.getElementById('activity') == 'Sedentary') {
        var tdee = ree * 1.2;
    }
    var tdee = ree * 2;

    document.getElementById('results').innerHTML = tdee;

}
