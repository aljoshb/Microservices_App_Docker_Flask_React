describe('Index', () => {

    it('users should be able to view the "/" page', () => {
        cy
            .visit('http://localhost')
            .get('h1').contains('All Users');
    });
});