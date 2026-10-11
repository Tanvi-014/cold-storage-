// Base URL of our Flask backend API
// Automatically adapts whether opened as a local file or served from a web host
const API_URL = (window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1")
  ? `${window.location.origin}/api/items`
  : "http://127.0.0.1:5000/api/items";

// Fallback sample data for static previews (e.g. GitHub Pages preview when backend is not running)
const SAMPLE_ITEMS = [
  { item_id: "CS-101", item_name: "Fresh Apples", category: "Fruits", temperature: "4°C" },
  { item_id: "CS-102", item_name: "Frozen Fish", category: "Seafood", temperature: "-18°C" },
  { item_id: "CS-103", item_name: "Dairy Butter", category: "Dairy", temperature: "-5°C" },
  { item_id: "CS-104", item_name: "Vaccines", category: "Pharmaceuticals", temperature: "2°C" }
];


// Helper function to render items into the HTML table
function renderTable(items) {
  const tbody = document.getElementById("itemTableBody");
  tbody.innerHTML = "";

  if (!items || items.length === 0) {
    tbody.innerHTML = `<tr><td colspan="5" class="no-records">No items in cold storage database.</td></tr>`;
    return;
  }

  items.forEach(item => {
    const row = document.createElement("tr");
    row.innerHTML = `
      <td><strong>${item.item_id}</strong></td>
      <td>${item.item_name}</td>
      <td>${item.category}</td>
      <td><span style="color: #0066cc; font-weight: bold;">${item.temperature}</span></td>
      <td>
        <button class="btn btn-edit" onclick="startEdit('${item.item_id}', '${escapeQuotes(item.item_name)}', '${escapeQuotes(item.category)}', '${escapeQuotes(item.temperature)}')">Edit</button>
        <button class="btn btn-del" onclick="deleteItem('${item.item_id}')">Delete</button>
      </td>
    `;
    tbody.appendChild(row);
  });
}


// 1. READ: Load all cold storage items from database
function loadItems() {
  fetch(API_URL)
    .then(response => response.json())
    .then(result => {
      renderTable(result.data || []);
    })
    .catch(error => {
      console.warn("Backend offline or unreachable, using sample data:", error);
      renderTable(SAMPLE_ITEMS);
      showMessage("Displaying cached database items. (Run backend server for live SQL updates)", "error");
    });
}


// 2. CREATE: Add a new cold storage item
function addItem() {
  const itemId = document.getElementById("itemId").value.trim();
  const itemName = document.getElementById("itemName").value.trim();
  const category = document.getElementById("category").value.trim();
  const temperature = document.getElementById("temperature").value.trim();

  // Validate form fields
  if (!itemId || !itemName || !category || !temperature) {
    showMessage("Please fill in all fields (Item ID, Name, Category, and Temperature).", "error");
    return;
  }

  // Send POST request with JSON body to backend
  fetch(API_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      item_id: itemId,
      item_name: itemName,
      category: category,
      temperature: temperature
    })
  })
    .then(response => response.json())
    .then(result => {
      if (result.success) {
        showMessage(result.message, "success");
        resetForm();
        loadItems(); // Refresh table to show new record
      } else {
        showMessage(result.message, "error");
      }
    })
    .catch(error => {
      console.error("Error adding item:", error);
      showMessage("Failed to connect to backend server. Make sure backend/app.py is running!", "error");
    });
}


// 3. EDIT PREPARATION: Populate form fields for editing
function startEdit(itemId, itemName, category, temperature) {
  document.getElementById("itemId").value = itemId;
  document.getElementById("itemId").disabled = true; // Primary Key cannot be changed
  document.getElementById("itemName").value = itemName;
  document.getElementById("category").value = category;
  document.getElementById("temperature").value = temperature;

  // Toggle buttons
  document.getElementById("btnAdd").style.display = "none";
  document.getElementById("btnUpdate").style.display = "inline-block";
  document.getElementById("formTitle").innerText = `Update Storage Item (${itemId})`;
}


// 4. UPDATE: Save updated details of an item
function updateItem() {
  const itemId = document.getElementById("itemId").value.trim();
  const itemName = document.getElementById("itemName").value.trim();
  const category = document.getElementById("category").value.trim();
  const temperature = document.getElementById("temperature").value.trim();

  if (!itemName || !category || !temperature) {
    showMessage("Name, Category, and Temperature cannot be empty.", "error");
    return;
  }

  // Send PUT request with updated data
  fetch(`${API_URL}/${itemId}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      item_name: itemName,
      category: category,
      temperature: temperature
    })
  })
    .then(response => response.json())
    .then(result => {
      if (result.success) {
        showMessage(result.message, "success");
        resetForm();
        loadItems(); // Refresh table with updated data
      } else {
        showMessage(result.message, "error");
      }
    })
    .catch(error => {
      console.error("Error updating item:", error);
      showMessage("Failed to update item. Make sure backend/app.py is running!", "error");
    });
}


// 5. DELETE: Remove an item from cold storage
function deleteItem(itemId) {
  const confirmed = confirm(`Are you sure you want to remove item '${itemId}' from cold storage?`);
  if (!confirmed) return;

  // Send DELETE request to backend API
  fetch(`${API_URL}/${itemId}`, {
    method: "DELETE"
  })
    .then(response => response.json())
    .then(result => {
      if (result.success) {
        showMessage(result.message, "success");
        loadItems(); // Refresh table
      } else {
        showMessage(result.message, "error");
      }
    })
    .catch(error => {
      console.error("Error deleting item:", error);
      showMessage("Failed to delete item. Make sure backend/app.py is running!", "error");
    });
}


// Reset the form back to initial state
function resetForm() {
  document.getElementById("itemForm").reset();
  const itemIdInput = document.getElementById("itemId");
  itemIdInput.disabled = false;

  document.getElementById("btnAdd").style.display = "inline-block";
  document.getElementById("btnUpdate").style.display = "none";
  document.getElementById("formTitle").innerText = "Add New Item to Storage";
}


// Display temporary alert message (success or error)
function showMessage(text, type) {
  const banner = document.getElementById("statusMessage");
  banner.className = `message-banner ${type}`;
  banner.innerText = text;
  banner.style.display = "block";

  // Automatically hide message after 4 seconds
  setTimeout(() => {
    banner.style.display = "none";
  }, 4000);
}


// Helper to escape special quotes for inline HTML onclick attributes
function escapeQuotes(str) {
  return (str || "").replace(/'/g, "\\'");
}


// Automatically load items when web page finishes loading
window.onload = loadItems;
