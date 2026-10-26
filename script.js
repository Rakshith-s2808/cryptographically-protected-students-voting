
const openVote = document.getElementById("openVote");
const closeVote = document.getElementById("closeVote");
const votingPanel = document.getElementById("votingPanel");
const demoSubmit = document.getElementById("demoSubmit");
const voteMessage = document.getElementById("voteMessage");
const receiptForm = document.getElementById("receiptForm");
const receiptCode = document.getElementById("receiptCode");
const receiptMessage = document.getElementById("receiptMessage");

openVote.addEventListener("click", () => {
    votingPanel.classList.remove("hidden");
    votingPanel.scrollIntoView({
        behavior: "smooth",
        block: "start"
    });
});

closeVote.addEventListener("click", () => {
    votingPanel.classList.add("hidden");
    voteMessage.textContent = "";
});

demoSubmit.addEventListener("click", () => {
    const selected = document.querySelector(
        'input[name="candidate"]:checked'
    );

    if (!selected) {
        voteMessage.textContent =
            "Please select a demo candidate first.";
        return;
    }

    // This is only a frontend demonstration.
    // No ballot is encrypted, saved, or submitted.
    voteMessage.textContent =
        `Demo selection: ${selected.value}. ` +
        "No real vote was cast. The cryptographic backend " +
        "will be connected in a later stage.";
});

receiptForm.addEventListener("submit", (event) => {
    event.preventDefault();

    const code = receiptCode.value.trim();

    if (!code) {
        receiptMessage.textContent =
            "Please enter a receipt code.";
        return;
    }

    // Never claim a receipt is valid without checking
    // actual ballot records on the backend.
    receiptMessage.textContent =
        "Demo only: no ballot records are connected. " +
        "This code has not been verified.";
});
