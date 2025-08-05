import streamlit as st
import pandas as pd
from aggrid_classes import Edit_Class, View_Class  # Import the classes from the main file

st.set_page_config(layout="wide")

def create_sample_data():
    """Create sample data for examples"""
    return pd.DataFrame({
        'Name': ['Alice Johnson', 'Bob Smith', 'Charlie Brown', 'Diana Prince', 'Eve Wilson'] * 6,
        'Age': [25, 30, 35, 28, 32] * 6,
        'City': ['New York', 'London', 'Tokyo', 'Paris', 'Sydney'] * 6,
        'Salary': [50000, 60000, 70000, 55000, 65000] * 6,
        'Department': ['IT', 'HR', 'Finance', 'Marketing', 'Operations'] * 6,
        'Performance': ['Excellent', 'Good', 'Outstanding', 'Good', 'Excellent'] * 6
    })

st.title("🎨 AG-Grid Styling Examples")
st.markdown("Three different styling approaches for the AG-Grid classes")

# Create tabs for the three examples
tab1, tab2, tab3 = st.tabs(["🔵 Ocean Blue Theme", "🟢 Forest Green Theme", "🟣 Royal Purple Theme"])

with tab1:
    st.header("🔵 Ocean Blue Theme Example")
    st.markdown("*Professional and calm blue styling*")
    
    # Example 1: Ocean Blue Theme
    sample_data = create_sample_data()
    
    blue_viewer = View_Class(
        df=sample_data,
        theme='balham',           # Professional theme
        height=500,              # Taller for more rows
        page_size=15,            # Custom page size
        cell_color='#1e3a8a',    # Deep blue text
        font_size='15px',        # Slightly smaller font
        font_family='Inter, system-ui, sans-serif'  # Modern font
    )
    
    blue_viewer.run(
        title="Employee Database - Ocean Theme", 
        description="A calming blue theme perfect for corporate data viewing"
    )
    
    # Show how to customize after creation
    st.info("**Customization Applied:** Deep blue text (#1e3a8a), Inter font, Balham theme, 15 rows per page")

with tab2:
    st.header("🟢 Forest Green Theme Example")
    st.markdown("*Natural and fresh green styling*")
    
    # Example 2: Forest Green Theme
    green_data = pd.DataFrame({
        'Project': ['Website Redesign', 'Mobile App', 'Database Migration', 'API Development', 'Testing Suite'] * 6,
        'Status': ['In Progress', 'Completed', 'Planning', 'In Progress', 'Testing'] * 6,
        'Priority': ['High', 'Medium', 'Critical', 'Medium', 'Low'] * 6,
        'Budget': [25000, 15000, 35000, 20000, 10000] * 6,
        'Team_Size': [5, 3, 8, 4, 2] * 6,
        'Deadline': ['2024-12-01', '2024-11-15', '2024-12-31', '2024-11-30', '2024-12-15'] * 6
    })
    
    green_viewer = View_Class(
        df=green_data,
        theme='alpine',          # Clean Alpine theme
        height=450,             # Standard height
        page_size=10,           # Default page size
        cell_color='#15803d',   # Forest green text
        font_size='16px',       # Standard font size
        font_family='Segoe UI, Tahoma, Geneva, Verdana, sans-serif'  # Windows-friendly fonts
    )
    
    green_viewer.run(
        title="Project Management - Forest Theme",
        description="Fresh green theme ideal for project tracking and nature-related data"
    )
    
    st.info("**Customization Applied:** Forest green text (#15803d), Segoe UI font family, Alpine theme, 10 rows per page")

with tab3:
    st.header("🟣 Royal Purple Theme Example")
    st.markdown("*Elegant and luxurious purple styling*")
    
    # Example 3: Royal Purple Theme with Editable functionality
    st.subheader("Editable Table with Purple Styling")
    
    # Create an editable instance with purple theme
    purple_editor = Edit_Class(
        theme='material',        # Material design theme
        height=400,             # Compact height
        page_size=8,            # Smaller page size for elegance
        cell_color='#7c3aed',   # Royal purple text
        font_size='17px',       # Larger, more elegant font
        font_family='Georgia, "Times New Roman", serif'  # Elegant serif font
    )
    
    purple_editor.run()
    
    st.info("**Customization Applied:** Royal purple text (#7c3aed), Georgia serif font, Material theme, 8 rows per page")
    
    # Additional purple-themed view table
    st.subheader("Additional Purple View Table")
    
    luxury_data = pd.DataFrame({
        'Product': ['Diamond Ring', 'Gold Watch', 'Silk Scarf', 'Leather Bag', 'Pearl Necklace'] * 4,
        'Category': ['Jewelry', 'Accessories', 'Fashion', 'Bags', 'Jewelry'] * 4,
        'Price': [5000, 2500, 300, 800, 1200] * 4,
        'Brand': ['Luxury Co', 'Time Masters', 'Silk Dreams', 'Leather Works', 'Pearl Palace'] * 4,
        'Rating': [4.9, 4.7, 4.5, 4.8, 4.6] * 4
    })
    
    luxury_viewer = View_Class(
        df=luxury_data,
        theme='material',
        height=350,
        page_size=5,
        cell_color='#9333ea',    # Slightly different purple shade
        font_size='16px',
        font_family='Playfair Display, Georgia, serif'  # Luxury serif font
    )
    
    luxury_viewer.run(
        title="Luxury Products Catalog",
        description="Premium purple theme for high-end product displays"
    )

# Add styling tips section
st.markdown("---")
st.header("🎨 Styling Customization Guide")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("🎨 Color Options")
    st.code("""
# Popular color schemes:
cell_color='#1e3a8a'  # Ocean Blue
cell_color='#15803d'  # Forest Green  
cell_color='#7c3aed'  # Royal Purple
cell_color='#dc2626'  # Crimson Red
cell_color='#ea580c'  # Vibrant Orange
cell_color='#0891b2'  # Cyan Blue
    """)

with col2:
    st.subheader("🔤 Font Families")
    st.code("""
# Font options:
font_family='Inter, sans-serif'
font_family='Segoe UI, sans-serif'  
font_family='Georgia, serif'
font_family='Roboto, sans-serif'
font_family='Playfair Display, serif'
font_family='Monospace'
    """)

with col3:
    st.subheader("🎭 Available Themes")
    st.code("""
# AG-Grid themes:
theme='alpine'     # Clean & modern
theme='balham'     # Professional
theme='material'   # Google Material
theme='fresh'      # Light & airy
theme='dark'       # Dark mode
theme='blue'       # Blue accent
    """)

st.markdown("---")
st.markdown("**💡 Pro Tip:** You can change these properties after creating the object by directly modifying the class attributes before calling `run()`")

# Example of post-creation customization
st.subheader("📝 Example: Changing Style After Creation")
st.code("""
# Create viewer with default settings
viewer = View_Class(df=your_data)

# Customize after creation
viewer.cell_color = '#dc2626'      # Change to red
viewer.font_size = '18px'          # Increase font size
viewer.theme = 'dark'              # Switch to dark theme
viewer.page_size = 25              # Change page size

# Then run with new settings
viewer.run("Custom Styled Table", "Modified after creation")
""")
