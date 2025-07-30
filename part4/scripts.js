document.addEventListener('DOMContentLoaded', () => {
    // ÉTAPE 1: Détecter sur quelle page on est
    const currentPage = window.location.pathname.split('/').pop();
    console.log('Page actuelle:', currentPage);
    
    // Si on est sur la page login
    if (currentPage === 'login.html') {
        console.log('On est sur la page login !');
        // Ici on va ajouter le code pour le login
    }
});