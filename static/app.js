new Vue({
    el: '#app',
    data: {
        naturalPrompt: '',
        plotUrl: '',
        errorMessage: '',
        isLoading: false
    },
    methods: {
        submitPrompt() {
            this.errorMessage = '';
            this.plotUrl = '';
            this.isLoading = true;

            fetch('/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    prompt: this.naturalPrompt
                }),
            })
            .then(response => {
                if (!response.ok) {
                    return response.json().then(data => { throw data.error; });
                }
                return response.json();
            })
            .then(data => {
                if (data.plot_url) {
                    this.plotUrl = data.plot_url;
                }
            })
            .catch(error => {
                this.errorMessage = error || 'An error occurred while processing your request.';
                console.error('Error:', error);
            })
            .finally(() => {
                this.isLoading = false;
            });
        }
    }
}); 