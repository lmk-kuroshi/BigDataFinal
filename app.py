import streamlit as st
import nbformat
import base64
from PIL import Image
from io import BytesIO

custom_labels = [
    "Total Sales Over Time",
    "Distribution of Sales",
    "Distribution of Quantity Ordered",
    "Distribution of Price Each",
    "Sales by Product Line",
    "Order Status Distribution",
    "Sales vs Quantity Ordered",
    "Sales vs Price Each",
    "Total Sales by Month",
    "Correlation Matrix",
    "Total Sales by Month",
    "Total Sales with Moving Average",
    "Sales with Outliers",
    "Sales with Outliers Replaced"
]

# Load notebook
notebook_path = "notebook2a262f01cb.ipynb"
with open(notebook_path, "r", encoding="utf-8") as f:
    nb = nbformat.read(f, as_version=4)

# Trích xuất ảnh từ notebook
images = []
for i, cell in enumerate(nb.cells):
    if cell.cell_type == 'code' and 'outputs' in cell:
        for output in cell['outputs']:
            if output.output_type in ['display_data', 'execute_result']:
                data = output.get('data', {})
                if 'image/png' in data:
                    img_bytes = base64.b64decode(data['image/png'])
                    # Tạo thumbnail
                    thumb = Image.open(BytesIO(img_bytes)).copy()
                    thumb.thumbnail((80, 80))
                    buffer = BytesIO()
                    thumb.save(buffer, format="PNG")
                    thumb_bytes = buffer.getvalue()
                    
                    # Gán tên tùy chỉnh nếu có
                    label = custom_labels[len(images)] if len(images) < len(custom_labels) else f"Hình {len(images)+1}"
                    
                    images.append({
                        "index": len(images),
                        "image": img_bytes,
                        "thumbnail": thumb_bytes,
                        "label": label
                    })

if not images:
    st.warning("Không có hình ảnh nào trong notebook.")
    st.stop()

# Init trạng thái
if 'selected_index' not in st.session_state:
    st.session_state.selected_index = 0

# === SIDEBAR (KHÔNG highlight) ===
st.sidebar.title("📁 Danh sách hình ảnh")
for img in images:
    cols = st.sidebar.columns([1, 4])
    with cols[0]:
        st.image(img["thumbnail"])
    with cols[1]:
        if cols[1].button(img["label"], key=f"btn_{img['index']}"):
            st.session_state.selected_index = img["index"]

# === MAIN ===
current_img = images[st.session_state.selected_index]
st.title(current_img["label"])
st.image(current_img["image"], use_container_width=True)