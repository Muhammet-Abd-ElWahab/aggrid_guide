import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode, JsCode

class Aggrid_Class:
    """Base class for AG-Grid configuration with all common options and styling"""
    
    def __init__(self, theme='alpine', height=450, page_size=20, cell_color='#008080', 
                 font_size='16px', font_family='Arial, sans-serif'):
        self.theme = theme
        self.height = height
        self.page_size = page_size
        self.cell_color = cell_color
        self.font_size = font_size
        self.font_family = font_family
        self.page_size_options = [5, 10, 20, 50, 100]
        
        # Ensure page_size is in the options
        if self.page_size not in self.page_size_options:
            self.page_size_options.append(self.page_size)
            self.page_size_options.sort()
    
    def configure_base_grid_options(self, df, editable=False, selection_mode=None, use_checkbox=False):
        """Configure base grid options with common settings"""
        gb = GridOptionsBuilder.from_dataframe(df)
        
        # Configure selection if needed
        if selection_mode:
            gb.configure_selection(selection_mode=selection_mode, use_checkbox=use_checkbox)
        
        # Hide row ID column
        gb.configure_column("__row_id__", hide=True)
        
        # Configure columns with styling
        for col in df.columns:
            if col != "__row_id__":
                gb.configure_column(
                    col,
                    editable=editable,
                    cellStyle={
                        'textAlign': 'left', 
                        'fontSize': self.font_size, 
                        'fontFamily': self.font_family, 
                        'color': self.cell_color
                    },
                    headerClass="left-header"
                )
        
        # Configure pagination and other grid options
        gb.configure_grid_options(
            domLayout='normal', 
            pagination=True, 
            paginationPageSize=self.page_size,
            paginationPageSizeSelector=self.page_size_options
        )
        gb.configure_side_bar()
        
        grid_options = gb.build()
        
        # Set default column definitions
        grid_options["defaultColDef"] = {
            "flex": 1, 
            "minWidth": 100, 
            "resizable": True, 
            "filter": True, 
            "sortable": True,
            "editable": editable,
            "headerClass": "left-header", 
            "cellStyle": {'textAlign': 'left'}
        }
        
        if editable:
            grid_options["singleClickEdit"] = True
        
        return grid_options
    
    def display_message(self, message_type=None, message_content="", position="bottom"):
        """Display messages with proper positioning"""
        if message_type and message_content:
            if position == "bottom":
                # Messages will be displayed after the grid
                pass
            else:
                # Display at top
                if message_type == "success":
                    st.success(message_content)
                elif message_type == "warning":
                    st.warning(message_content)
                elif message_type == "error":
                    st.error(message_content)
                elif message_type == "info":
                    st.info(message_content)
    
    def show_bottom_message(self):
        """Show message at bottom of the page"""
        if hasattr(st.session_state, 'message_type') and st.session_state.message_type:
            if st.session_state.message_type == "success":
                st.success(st.session_state.message_content)
            elif st.session_state.message_type == "warning":
                st.warning(st.session_state.message_content)
            elif st.session_state.message_type == "error":
                st.error(st.session_state.message_content)
            elif st.session_state.message_type == "info":
                st.info(st.session_state.message_content)
            
            # Clear the message after displaying
            st.session_state.message_type = None
            st.session_state.message_content = ""

class Edit_Class(Aggrid_Class):
    """Class for editable AG-Grid tables, inherited from Aggrid_Class"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.initialize_session_state()
    
    def initialize_session_state(self):
        """Initialize session state variables for editing functionality"""
        if "main_df" not in st.session_state:
            df_initial = pd.DataFrame({
                'Name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve', 'Alice', 'Bob', 'Charlie', 'Diana', 'Eve'],
                'Age': [25, 30, 35, 28, 32, 25, 30, 35, 28, 32],
                'City': ['New York', 'London', 'Tokyo', 'Paris', 'Sydney', 'New York', 'London', 'Tokyo', 'Paris', 'Sydney'],
                'Salary': [50000, 60000, 70000, 55000, 65000, 50000, 60000, 70000, 55000, 65000],
                'Department': ['IT', 'HR', 'Finance', 'IT', 'Marketing', 'IT', 'HR', 'Finance', 'IT', 'Marketing']
            })
            df_initial["__row_id__"] = df_initial.index
            st.session_state.main_df = df_initial.copy()

        if "view_mode" not in st.session_state:
            st.session_state.view_mode = "full_table"

        if "selected_rows_for_editing" not in st.session_state:
            st.session_state.selected_rows_for_editing = pd.DataFrame()

        if "message_type" not in st.session_state:
            st.session_state.message_type = None
        if "message_content" not in st.session_state:
            st.session_state.message_content = ""
    
    def display_full_table(self):
        """Display the full table with row selection for editing"""
        st.header("Full Data Table: Select Rows to Edit")
        st.markdown("Use the checkboxes to select rows, then click 'Edit Selected Rows'.")

        df_display_full = st.session_state.main_df.copy()

        # Configure grid options for selection
        grid_options_full = self.configure_base_grid_options(
            df_display_full, 
            editable=False, 
            selection_mode="multiple", 
            use_checkbox=True
        )

        # Display the grid
        grid_response_full = AgGrid(
            df_display_full,
            gridOptions=grid_options_full,
            update_mode=GridUpdateMode.SELECTION_CHANGED,
            data_return_mode=DataReturnMode.AS_INPUT,
            height=self.height,
            allow_unsafe_jscode=False,
            enable_enterprise_modules=True,
            theme=self.theme,
            fit_columns_on_grid_load=True,
            key="full_table_grid",
            reload_data=False
        )

        selected_rows_from_full_grid_list = grid_response_full.get("selected_rows", [])
        
        st.markdown("---")
        if st.button("Edit Selected Rows"):
            df_selected_for_check = pd.DataFrame(selected_rows_from_full_grid_list)

            if not df_selected_for_check.empty:
                st.session_state.selected_rows_for_editing = df_selected_for_check
                st.session_state.view_mode = "selected_table_editing"
                st.session_state.message_type = "info"
                st.session_state.message_content = f"✏️ Editing {len(df_selected_for_check)} selected row(s)."
                st.rerun()
            else:
                st.session_state.message_type = "warning"
                st.session_state.message_content = "⚠️ No rows selected. Please select rows to edit."
                st.rerun()
        
        # Show messages at bottom
        self.show_bottom_message()
    
    def display_editing_table(self):
        """Display the selected rows for editing"""
        st.header("Edit Selected Rows")
        st.markdown("Edit the cells below. All cells in this table are editable.")

        df_selected_edit = st.session_state.selected_rows_for_editing.copy()

        # Configure grid options for editing
        grid_options_selected = self.configure_base_grid_options(
            df_selected_edit, 
            editable=True
        )

        # Display the editable grid
        grid_response_selected = AgGrid(
            df_selected_edit,
            gridOptions=grid_options_selected,
            update_mode=GridUpdateMode.VALUE_CHANGED,
            data_return_mode=DataReturnMode.AS_INPUT,
            height=self.height,
            allow_unsafe_jscode=False,
            enable_enterprise_modules=True,
            theme=self.theme,
            fit_columns_on_grid_load=True,
            key="selected_table_editing_grid",
            reload_data=False
        )

        edited_selected_df = pd.DataFrame(grid_response_selected["data"])

        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Submit Changes"):
                self.submit_changes(edited_selected_df)
        
        with col2:
            if st.button("Cancel Editing"):
                st.session_state.message_type = "info"
                st.session_state.message_content = "ℹ️ Editing cancelled. No changes applied."
                st.session_state.view_mode = "full_table"
                st.rerun()
        
        # Show messages at bottom
        self.show_bottom_message()
    
    def submit_changes(self, edited_selected_df):
        """Submit the edited changes to the main dataframe"""
        if "__row_id__" not in edited_selected_df.columns:
            st.session_state.message_type = "error"
            st.session_state.message_content = "❌ Internal error: '__row_id__' column missing in edited data. Cannot process updates."
            st.rerun()
        else:
            selected_ids_to_update = edited_selected_df["__row_id__"].tolist()
            df_to_update = st.session_state.main_df.set_index("__row_id__").copy()
            edited_rows_indexed = edited_selected_df.set_index("__row_id__")
            data_cols_for_update = [col for col in edited_selected_df.columns if col != "__row_id__"]
            
            # Check if any actual changes were made
            current_selected_data_in_main_df = df_to_update.loc[selected_ids_to_update, data_cols_for_update]
            if edited_rows_indexed[data_cols_for_update].equals(current_selected_data_in_main_df):
                st.session_state.message_type = "info"
                st.session_state.message_content = "ℹ️ No actual changes were made to the data in the selected rows."
            else:
                df_to_update.update(edited_rows_indexed[data_cols_for_update])
                st.session_state.main_df = df_to_update.reset_index()
                st.session_state.message_type = "success"
                st.session_state.message_content = f"✅ Changes applied successfully to {len(selected_ids_to_update)} row(s)!"
            
            st.session_state.view_mode = "full_table"
            st.rerun()
    
    def run(self):
        """Main method to run the editing interface"""
        if st.session_state.view_mode == "full_table":
            self.display_full_table()
        elif st.session_state.view_mode == "selected_table_editing":
            self.display_editing_table()

class View_Class(Aggrid_Class):
    """Class for read-only AG-Grid tables, inherited from Aggrid_Class"""
    
    def __init__(self, df=None, **kwargs):
        super().__init__(**kwargs)
        if df is not None:
            self.df = df.copy()
            if "__row_id__" not in self.df.columns:
                self.df["__row_id__"] = self.df.index
        else:
            self.df = self.create_sample_data()
    
    def create_sample_data(self):
        """Create sample data if no dataframe is provided"""
        df = pd.DataFrame({
            'Name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve'] * 4,
            'Age': [25, 30, 35, 28, 32] * 4,
            'City': ['New York', 'London', 'Tokyo', 'Paris', 'Sydney'] * 4,
            'Salary': [50000, 60000, 70000, 55000, 65000] * 4,
            'Department': ['IT', 'HR', 'Finance', 'IT', 'Marketing'] * 4
        })
        df["__row_id__"] = df.index
        return df
    
    def display_view_table(self, title="Data View", description="Read-only view of the data"):
        """Display the dataframe in read-only mode"""
        st.header(title)
        st.markdown(description)

        # Configure grid options for viewing only
        grid_options = self.configure_base_grid_options(
            self.df, 
            editable=False
        )

        # Display the read-only grid
        AgGrid(
            self.df,
            gridOptions=grid_options,
            update_mode=GridUpdateMode.NO_UPDATE,
            data_return_mode=DataReturnMode.AS_INPUT,
            height=self.height,
            allow_unsafe_jscode=False,
            enable_enterprise_modules=True,
            theme=self.theme,
            fit_columns_on_grid_load=True,
            key=f"view_table_{id(self)}",
            reload_data=False
        )
        
        # Show messages at bottom if any
        self.show_bottom_message()
    
    def run(self, title="Data View", description="Read-only view of the data"):
        """Main method to run the view interface"""
        self.display_view_table(title, description)

# Example usage and customization
def example_usage():
    """Examples of using the classes with different colors and styles"""
    
    st.set_page_config(layout="wide")
    
    st.title("AG-Grid Classes Examples")
    
    # Create tabs for different examples
    tab1, tab2, tab3, tab4 = st.tabs(["Editable Table", "Blue Theme View", "Green Theme View", "Purple Theme View"])
    
    with tab1:
        st.subheader("Example 1: Editable Table (Default Style)")
        editor = Edit_Class()
        editor.run()
    
    with tab2:
        st.subheader("Example 2: Blue Theme View")
        # Create sample data
        sample_df = pd.DataFrame({
            'Product': ['Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Headphones'] * 4,
            'Price': [1200, 25, 75, 300, 150] * 4,
            'Category': ['Electronics', 'Accessories', 'Accessories', 'Electronics', 'Audio'] * 4,
            'Stock': [50, 200, 100, 30, 75] * 4
        })
        
        blue_viewer = View_Class(
            df=sample_df,
            theme='balham',
            height=500,
            page_size=10,
            cell_color='#1f4e79',
            font_size='14px',
            font_family='Segoe UI, sans-serif'
        )
        blue_viewer.run("Product Inventory", "Blue themed view of product data")
    
    with tab3:
        st.subheader("Example 3: Green Theme View")
        # Create different sample data
        green_df = pd.DataFrame({
            'Employee': ['John Doe', 'Jane Smith', 'Mike Johnson', 'Sarah Wilson', 'Tom Brown'] * 4,
            'Position': ['Manager', 'Developer', 'Designer', 'Analyst', 'Tester'] * 4,
            'Experience': [5, 3, 4, 2, 6] * 4,
            'Rating': [4.5, 4.2, 4.8, 4.0, 4.6] * 4
        })
        
        green_viewer = View_Class(
            df=green_df,
            theme='alpine',
            height=400,
            page_size=5,
            cell_color='#2d5a3d',
            font_size='15px',
            font_family='Georgia, serif'
        )
        green_viewer.run("Employee Records", "Green themed employee data view")
    
    with tab4:
        st.subheader("Example 4: Purple Theme View")
        # Create another sample data
        purple_df = pd.DataFrame({
            'Course': ['Python', 'JavaScript', 'React', 'SQL', 'Machine Learning'] * 4,
            'Duration': ['40 hours', '35 hours', '30 hours', '25 hours', '60 hours'] * 4,
            'Level': ['Beginner', 'Intermediate', 'Advanced', 'Beginner', 'Advanced'] * 4,
            'Students': [120, 85, 65, 95, 45] * 4
        })
        
        purple_viewer = View_Class(
            df=purple_df,
            theme='material',
            height=450,
            page_size=50,
            cell_color='#6a1b9a',
            font_size='16px',
            font_family='Roboto, sans-serif'
        )
        purple_viewer.run("Course Catalog", "Purple themed course information")

# Run the examples
if __name__ == "__main__":
    example_usage()