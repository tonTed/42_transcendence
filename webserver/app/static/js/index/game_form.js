
export function init_game_form() {
    const btn_1v1 = document.getElementById('1v1')
    const btn_tournament = document.getElementById('tournament')
    
    btn_1v1.addEventListener('click', function() {
        btn_1v1.classList.add('btn-success');
        btn_tournament.classList.remove('btn-success');
        document.getElementById('1v1-container').classList.remove('d-none');
        document.getElementById('tournament-container').classList.add('d-none');
    });
    
    btn_tournament.addEventListener('click', function() {
        btn_tournament.classList.add('btn-success');
        btn_1v1.classList.remove('btn-success');
        document.getElementById('1v1-container').classList.add('d-none');
        document.getElementById('tournament-container').classList.remove('d-none');
    });
}
