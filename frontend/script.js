const apiUrl = "http://localhost:8000";

async function loadInstances() {
  const res = await fetch(`${apiUrl}/instances_db`);
  const data = await res.json();
  const table = document.getElementById("instance-table");
  table.innerHTML = "";

  data.forEach(inst => {
    const row = document.createElement("tr");

    row.innerHTML = `
      <td>${inst.instance_id}</td>
      <td>${inst.status}</td>
      <td>${inst.version}</td>
      <td>${inst.last_heartbeat}</td>
      <td>
        <button onclick="sendCommand('${inst.instance_id}', 'restart')">Restart</button>
      </td>
    `;

    table.appendChild(row);
  });
}

async function sendCommand(instanceId, command) {
  const res = await fetch(`${apiUrl}/commands`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ instance_id: instanceId, command: command }),
  });
  const result = await res.json();
  alert(JSON.stringify(result));
}

loadInstances();
setInterval(loadInstances, 5000); // actualizare la fiecare 5 secunde
