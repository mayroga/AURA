const style = document.createElement("style");
style.textContent = `
body { font-family: Arial, sans-serif; padding: 20px; background: #f7f7f7; }
header { text-align: center; margin-bottom: 20px; }
input { display: block; margin: 10px 0; padding: 8px; width: 100%; max-width: 300px; }
button { padding: 10px 20px; margin: 5px; cursor: pointer; }
.planBtn { background: #0b5cff; color: #fff; border: none; border-radius: 4px; }
#estimateResult, #donationResult { margin-top: 15px; font-weight: bold; }
select { padding: 5px; margin-top: 5px; }
`;
document.head.appendChild(style);
