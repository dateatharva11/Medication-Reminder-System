function makeCall() {
  const phoneNumber = document.getElementById("phoneNumber").value;
  if (!phoneNumber) {
      alert("Please enter a phone number");
      return;
  }

  fetch("/call", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ phone_number: phoneNumber })
  })
  .then(response => response.json())
  .then(data => {
      document.getElementById("responseMessage").textContent = data.message;
  })
  .catch(error => console.error("Error:", error));
}
