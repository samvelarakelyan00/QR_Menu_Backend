document.addEventListener('DOMContentLoaded', () => {
    console.log("Script loaded and DOM is ready!");

    const tipSections = document.querySelectorAll('.tip-section');

    tipSections.forEach(section => {
        const buttons = section.querySelectorAll('.tip-amount');

        buttons.forEach(button => {
            button.addEventListener('click', () => {

                section.querySelectorAll('.tip-amount').forEach(btn => btn.classList.remove('selected'));
                button.classList.add('selected');
            });
        });

        // Select the default 300 button on page load (one per section)
        const defaultButton = section.querySelector('.tip-amount[data-amount="300"]');
        if (defaultButton) {
            defaultButton.classList.add('selected');
        }
    });

    document.getElementById('submit-tip').addEventListener('click', () => {

        const selectedTips = [];

        tipSections.forEach(section => {
            const selectedButton = section.querySelector('.tip-amount.selected');
            if (selectedButton) {
                selectedTips.push({
                    section: section.querySelector('h2').textContent.trim(),
                    amount: selectedButton.dataset.amount
                });
            }
        });

        console.log("Selected Tips:", selectedTips);
        alert(`Selected Tips:\n${selectedTips.map(tip => `${tip.section}: ${tip.amount}`).join("\n")}`);
    });
});