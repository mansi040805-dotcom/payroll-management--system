import os
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = Presentation()
    # 16:9 widescreen slides
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # Blank slide layout
    blank_layout = prs.slide_layouts[6]

    # Color Palette
    PRIMARY = RGBColor(30, 58, 138)       # Navy Blue #1E3A8A
    SECONDARY = RGBColor(37, 99, 235)    # Royal Blue #2563EB
    ACCENT = RGBColor(16, 185, 129)      # Emerald Green #10B981
    DARK_TEXT = RGBColor(31, 41, 55)     # Slate 800 #1F2937
    MUTED_TEXT = RGBColor(107, 114, 128) # Gray 500 #6B7280
    BG_LIGHT = RGBColor(248, 250, 252)   # Slate 50 #F8FAFC
    CARD_BG = RGBColor(255, 255, 255)    # White
    BORDER_COLOR = RGBColor(226, 232, 240) # Slate 200

    def add_header(slide, title_text, category_text="PAYROLL & COMPENSATION MANAGEMENT SYSTEM"):
        # Header banner or top accent
        top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.15))
        top_bar.fill.solid()
        top_bar.fill.fore_color.rgb = SECONDARY
        top_bar.line.fill.background()

        # Category / Tag
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.35))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.size = Pt(10)
        p_cat.font.bold = True
        p_cat.font.color.rgb = SECONDARY

        # Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.75), Inches(11.7), Inches(0.7))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.size = Pt(24)
        p_title.font.bold = True
        p_title.font.color.rgb = PRIMARY

    def add_card(slide, left, top, width, height, bg_color=CARD_BG, border_color=BORDER_COLOR):
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = bg_color
        if border_color:
            shape.line.color.rgb = border_color
            shape.line.width = Pt(1.5)
        else:
            shape.line.fill.background()
        return shape

    # ==========================================
    # SLIDE 1: TITLE SLIDE
    # ==========================================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = PRIMARY
    bg1.line.fill.background()

    # Title box
    t_box = s1.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.333), Inches(2.2))
    tf1 = t_box.text_frame
    tf1.word_wrap = True
    p1 = tf1.paragraphs[0]
    p1.text = "Payroll & Compensation\nManagement System"
    p1.font.size = Pt(40)
    p1.font.bold = True
    p1.font.color.rgb = RGBColor(255, 255, 255)
    p1.alignment = PP_ALIGN.LEFT

    # Subtitle box
    sub_box = s1.shapes.add_textbox(Inches(1.0), Inches(4.2), Inches(11.333), Inches(1.0))
    tf_sub = sub_box.text_frame
    p_sub = tf_sub.paragraphs[0]
    p_sub.text = "A Desktop Application Demonstrating Practical Object-Oriented Programming (OOP) in Python"
    p_sub.font.size = Pt(18)
    p_sub.font.color.rgb = RGBColor(147, 197, 253) # Light Blue

    # Footer Metadata Card
    card_meta = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(5.6), Inches(11.333), Inches(1.1))
    card_meta.fill.solid()
    card_meta.fill.fore_color.rgb = RGBColor(23, 37, 84) # Dark Navy
    card_meta.line.color.rgb = SECONDARY
    card_meta.line.width = Pt(1)

    tf_meta = card_meta.text_frame
    tf_meta.word_wrap = True
    p_m = tf_meta.paragraphs[0]
    p_m.text = "COURSE: Object-Oriented Programming (Semester Project)   |   TECH: Python 3, Tkinter GUI, JSON Persistence"
    p_m.font.size = Pt(12)
    p_m.font.bold = True
    p_m.font.color.rgb = RGBColor(255, 255, 255)
    p_m.alignment = PP_ALIGN.CENTER

    # ==========================================
    # SLIDE 2: PROBLEM STATEMENT & OBJECTIVES
    # ==========================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "Problem Statement & Project Objectives", "Context & Motivation")

    # Card 1: The Challenge (Left)
    add_card(s2, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2))
    box1 = s2.shapes.add_textbox(Inches(1.1), Inches(1.8), Inches(5.0), Inches(4.7))
    tf2_1 = box1.text_frame
    tf2_1.word_wrap = True
    
    p = tf2_1.paragraphs[0]
    p.text = "The Real-World Challenge"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = PRIMARY
    
    bullets_1 = [
        ("Manual Salary Calculations:", "Tracking work hours, absences, overtime, and allowances manually is error-prone and time-consuming."),
        ("Diverse Employment Types:", "Salaried workers need fixed monthly rules with leave deductions, while hourly staff get paid strictly for clocked hours."),
        ("Audit & Records Preservation:", "Historical finalized payments must never be accidentally overwritten when employee salary structures change."),
        ("No Bloated Tooling:", "Organizations and educational labs need lightweight, local systems that work offline without complex database servers.")
    ]
    for b_title, b_desc in bullets_1:
        p = tf2_1.add_paragraph()
        p.text = f"• {b_title} "
        p.font.bold = True
        p.font.size = Pt(13)
        p.font.color.rgb = DARK_TEXT
        run = p.add_run()
        run.text = b_desc
        run.font.bold = False
        run.font.color.rgb = MUTED_TEXT

    # Card 2: Core Objectives (Right)
    add_card(s2, Inches(6.9), Inches(1.6), Inches(5.6), Inches(5.2))
    box2 = s2.shapes.add_textbox(Inches(7.2), Inches(1.8), Inches(5.0), Inches(4.7))
    tf2_2 = box2.text_frame
    tf2_2.word_wrap = True
    
    p = tf2_2.paragraphs[0]
    p.text = "System Objectives"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = SECONDARY
    
    bullets_2 = [
        ("End-to-End Workflow:", "Integrate employee directory, daily attendance, leave management, compensation, payroll, and payment tracking."),
        ("Strict Technology Restrictions:", "Built exclusively with Python 3, native Tkinter GUI, and JSON file storage (No SQL, No Web Frameworks)."),
        ("Clear Academic OOP Design:", "Solve real business needs using clean, easily explainable OOP principles (Inheritance, Polymorphism, Composition)."),
        ("Robustness & Integrity:", "Include full validation, custom exception handling, and 30 automated unit tests guaranteeing 100% test coverage.")
    ]
    for b_title, b_desc in bullets_2:
        p = tf2_2.add_paragraph()
        p.text = f"✔ {b_title} "
        p.font.bold = True
        p.font.size = Pt(13)
        p.font.color.rgb = DARK_TEXT
        run = p.add_run()
        run.text = b_desc
        run.font.bold = False
        run.font.color.rgb = MUTED_TEXT

    # ==========================================
    # SLIDE 3: SYSTEM ARCHITECTURE & PROJECT STRUCTURE
    # ==========================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "System Architecture & Modular Structure", "Architecture & Organization")

    modules = [
        ("main.py", "Entry Point", "Initializes the application, automatically checks and seeds sample data on first run, and launches the Tkinter root loop."),
        ("employee.py", "Domain Hierarchy", "Defines the abstract Employee base class along with SalariedEmployee and HourlyEmployee subclasses."),
        ("records.py", "Associated Entities", "Implements Attendance (auto-calculating work hours), Leave requests, and Payment transaction records."),
        ("payroll.py", "Business Logic", "Contains SalaryBreakdown (composition), Payroll entity, and PayrollManager for salary calculation orchestration."),
        ("file_manager.py", "Persistence Layer", "Provides clean JSON CRUD operations and text payslip file export, completely separated from UI logic."),
        ("gui.py", "Presentation Layer", "A 8-tab Tkinter/ttk desktop GUI linking buttons and tables directly to backend domain manager methods.")
    ]

    card_coords = [
        (Inches(0.8), Inches(1.6)), (Inches(4.9), Inches(1.6)), (Inches(9.0), Inches(1.6)),
        (Inches(0.8), Inches(4.3)), (Inches(4.9), Inches(4.3)), (Inches(9.0), Inches(4.3))
    ]

    for idx, (m_file, m_role, m_desc) in enumerate(modules):
        x, y = card_coords[idx]
        add_card(s3, x, y, Inches(3.55), Inches(2.5))
        t_box = s3.shapes.add_textbox(x + Inches(0.2), y + Inches(0.2), Inches(3.15), Inches(2.1))
        tf = t_box.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = m_file
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.rgb = PRIMARY
        
        p_sub = tf.add_paragraph()
        p_sub.text = m_role.upper()
        p_sub.font.size = Pt(10)
        p_sub.font.bold = True
        p_sub.font.color.rgb = SECONDARY
        
        p_desc = tf.add_paragraph()
        p_desc.text = m_desc
        p_desc.font.size = Pt(11)
        p_desc.font.color.rgb = DARK_TEXT

    # ==========================================
    # SLIDE 4: CORE OOP CONCEPTS - INHERITANCE & ABSTRACTION
    # ==========================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "Core OOP: Abstraction & Inheritance Hierarchy", "OOP Concept 1 & 2")

    # Left Card: Abstract Employee Class
    add_card(s4, Inches(0.8), Inches(1.6), Inches(4.8), Inches(5.2))
    b_left = s4.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(4.4), Inches(4.8))
    tf4_l = b_left.text_frame
    tf4_l.word_wrap = True
    
    p = tf4_l.paragraphs[0]
    p.text = "Abstract Base Class: Employee"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = PRIMARY
    
    p_code = tf4_l.add_paragraph()
    p_code.text = "class Employee(ABC):\n    # Common Protected Attributes\n    _employee_id, _name, _email,\n    _department, _designation\n\n    @abstractmethod\n    def calculate_salary(self, att, comp):\n        pass\n\n    @abstractmethod\n    def get_base_pay_info(self):\n        pass"
    p_code.font.size = Pt(11)
    p_code.font.name = "Consolas"
    p_code.font.color.rgb = RGBColor(30, 64, 175)

    p_exp = tf4_l.add_paragraph()
    p_exp.text = "\n• Abstraction Concept: Employee cannot be instantiated directly; it defines a mandatory blueprint for all employee types."
    p_exp.font.size = Pt(12)
    p_exp.font.color.rgb = DARK_TEXT

    # Right Card: Salaried vs Hourly Subclasses
    add_card(s4, Inches(6.0), Inches(1.6), Inches(6.5), Inches(5.2))
    b_right = s4.shapes.add_textbox(Inches(6.3), Inches(1.8), Inches(6.0), Inches(4.8))
    tf4_r = b_right.text_frame
    tf4_r.word_wrap = True
    
    p = tf4_r.paragraphs[0]
    p.text = "Inheritance & Constructor Extension"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = SECONDARY
    
    items = [
        ("SalariedEmployee(Employee)", "Inherits common attributes using super().__init__(...).\nAdds private __basic_salary (fixed monthly pay).\nCalculates daily & hourly rates to compute unpaid leave & overtime."),
        ("HourlyEmployee(Employee)", "Inherits common attributes using super().__init__(...).\nAdds private __hourly_rate.\nCalculates pay strictly by multiplying clocked regular hours + overtime."),
        ("Code Reusability & DRY Principle", "All identity, contact, department, status, and dictionary serialization logic resides in Employee, eliminating code duplication.")
    ]
    for h, desc in items:
        p_h = tf4_r.add_paragraph()
        p_h.text = f"▶ {h}"
        p_h.font.bold = True
        p_h.font.size = Pt(13)
        p_h.font.color.rgb = PRIMARY
        p_d = tf4_r.add_paragraph()
        p_d.text = desc
        p_d.font.size = Pt(11)
        p_d.font.color.rgb = DARK_TEXT

    # ==========================================
    # SLIDE 5: POLYMORPHISM IN ACTION
    # ==========================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "Polymorphism: Dynamic Runtime Salary Calculation", "OOP Concept 3")

    # Top Explanation Card
    add_card(s5, Inches(0.8), Inches(1.6), Inches(11.7), Inches(1.3), bg_color=RGBColor(239, 246, 255), border_color=SECONDARY)
    b_top = s5.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(11.3), Inches(1.1))
    tf5_t = b_top.text_frame
    tf5_t.word_wrap = True
    p = tf5_t.paragraphs[0]
    p.text = "What is Runtime Polymorphism in this Project?"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = PRIMARY
    p2 = tf5_t.add_paragraph()
    p2.text = "The PayrollManager loops over a list of Employee objects and calls 'employee.calculate_salary(...)'. Python automatically dispatches to the correct subclass method at runtime without any if/else type checks!"
    p2.font.size = Pt(12)
    p2.font.color.rgb = DARK_TEXT

    # Column 1: Salaried Method (Left)
    add_card(s5, Inches(0.8), Inches(3.1), Inches(5.6), Inches(3.7))
    b_col1 = s5.shapes.add_textbox(Inches(1.0), Inches(3.3), Inches(5.2), Inches(3.3))
    tf5_c1 = b_col1.text_frame
    tf5_c1.word_wrap = True
    p = tf5_c1.paragraphs[0]
    p.text = "SalariedEmployee.calculate_salary()"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = PRIMARY

    sal_formulas = [
        "Gross = Basic Salary + Allowances + Bonus + OT",
        "Daily Rate = Basic Salary / 22 Working Days",
        "Unpaid Leave Deduction = Daily Rate × Unpaid Days",
        "Absence Deduction = Daily Rate × (Absences + 0.5 × HalfDays)",
        "Overtime Pay = OT Hours × Hourly Rate × 1.5",
        "Net Salary = Gross - Total Deductions"
    ]
    for f in sal_formulas:
        p = tf5_c1.add_paragraph()
        p.text = f"• {f}"
        p.font.size = Pt(11)
        p.font.color.rgb = DARK_TEXT

    # Column 2: Hourly Method (Right)
    add_card(s5, Inches(6.9), Inches(3.1), Inches(5.6), Inches(3.7))
    b_col2 = s5.shapes.add_textbox(Inches(7.1), Inches(3.3), Inches(5.2), Inches(3.3))
    tf5_c2 = b_col2.text_frame
    tf5_c2.word_wrap = True
    p = tf5_c2.paragraphs[0]
    p.text = "HourlyEmployee.calculate_salary()"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = SECONDARY

    hr_formulas = [
        "Regular Hours = Total Hours - Overtime Hours",
        "Regular Pay = Regular Hours × Hourly Rate",
        "Overtime Pay = OT Hours × Hourly Rate × 1.5",
        "Gross Salary = Regular Pay + OT Pay + Allowances + Bonus",
        "Deductions = Other Misc Deductions only",
        "Net Salary = Gross - Deductions",
        "(Note: No absence deductions; pay is purely hour-based)"
    ]
    for f in hr_formulas:
        p = tf5_c2.add_paragraph()
        p.text = f"• {f}"
        p.font.size = Pt(11)
        p.font.color.rgb = DARK_TEXT

    # ==========================================
    # SLIDE 6: ENCAPSULATION & OBJECT RELATIONSHIPS
    # ==========================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Encapsulation & Object Relationships", "OOP Concepts 4, 5 & 6")

    rel_cards = [
        ("Encapsulation & Data Hiding", "Private/Protected Attributes & Getters/Setters", 
         "• Attributes use _attribute (protected) and __attribute (private).\n• @property and @setter validate incoming values (e.g., salary cannot be negative, name cannot be empty).\n• Restricts direct external state tampering.",
         Inches(0.8), Inches(1.6), Inches(5.6), Inches(2.5)),
        
        ("Composition (Part-Of Relationship)", "Payroll owns SalaryBreakdown", 
         "• Payroll creates a SalaryBreakdown object upon initialization.\n• SalaryBreakdown cannot exist independently outside of Payroll.\n• If a Payroll record is deleted, its breakdown is deleted with it.",
         Inches(6.9), Inches(1.6), Inches(5.6), Inches(2.5)),

        ("Aggregation (Has-A Relationship)", "PayrollManager uses FileManager & Employee", 
         "• PayrollManager maintains a reference to FileManager to read/write records.\n• FileManager and Employee exist independently outside PayrollManager lifecycle.\n• Clean separation of processing vs storage.",
         Inches(0.8), Inches(4.3), Inches(5.6), Inches(2.5)),

        ("Association (Loose Coupling)", "Attendance & Leave link to Employee", 
         "• Attendance, Leave, and Payment associate with Employee via employee_id.\n• Keeps record models modular, lightweight, and easily serializable to JSON without circular object references.",
         Inches(6.9), Inches(4.3), Inches(5.6), Inches(2.5))
    ]

    for title, sub, body, x, y, w, h in rel_cards:
        add_card(s6, x, y, w, h)
        tb = s6.shapes.add_textbox(x + Inches(0.2), y + Inches(0.15), w - Inches(0.4), h - Inches(0.3))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = PRIMARY
        
        p_sub = tf.add_paragraph()
        p_sub.text = sub.upper()
        p_sub.font.size = Pt(10)
        p_sub.font.bold = True
        p_sub.font.color.rgb = SECONDARY
        
        p_b = tf.add_paragraph()
        p_b.text = body
        p_b.font.size = Pt(11)
        p_b.font.color.rgb = DARK_TEXT

    # ==========================================
    # SLIDE 7: DATA PERSISTENCE & ERROR HANDLING
    # ==========================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "JSON Data Persistence & Exception Handling", "Persistence & Reliability")

    # Left Card: JSON Persistence
    add_card(s7, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2))
    b_p = s7.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.2), Inches(4.8))
    tf7_l = b_p.text_frame
    tf7_l.word_wrap = True
    
    p = tf7_l.paragraphs[0]
    p.text = "FileManager & JSON Storage"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = PRIMARY
    
    p_sub = tf7_l.add_paragraph()
    p_sub.text = "DATA PERSISTENCE WITHOUT HEAVY DATABASES"
    p_sub.font.size = Pt(10)
    p_sub.font.bold = True
    p_sub.font.color.rgb = SECONDARY

    points_persist = [
        ("Modular File Structure:", "Individual JSON files for employees, attendance, leaves, compensation, payroll, and payments."),
        ("Auto-Initialization:", "Creates the data/ and payslips/ directories automatically if missing upon launch."),
        ("Full CRUD Capabilities:", "read_data(), write_data(), add_record(), update_record(), delete_record(), find_record()."),
        ("Audit Lock & State Preservation:", "Once payroll is marked 'Finalized', historical values are preserved even if current employee pay changes.")
    ]
    for t, d in points_persist:
        p = tf7_l.add_paragraph()
        p.text = f"• {t} "
        p.font.bold = True
        p.font.size = Pt(12)
        p.font.color.rgb = DARK_TEXT
        r = p.add_run()
        r.text = d
        r.font.bold = False
        r.font.color.rgb = MUTED_TEXT

    # Right Card: Custom Exceptions
    add_card(s7, Inches(6.9), Inches(1.6), Inches(5.6), Inches(5.2))
    b_e = s7.shapes.add_textbox(Inches(7.1), Inches(1.8), Inches(5.2), Inches(4.8))
    tf7_r = b_e.text_frame
    tf7_r.word_wrap = True
    
    p = tf7_r.paragraphs[0]
    p.text = "Custom Exception Hierarchy"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = PRIMARY
    
    p_sub = tf7_r.add_paragraph()
    p_sub.text = "DOMAIN VALIDATION & CLEAN RECOVERY"
    p_sub.font.size = Pt(10)
    p_sub.font.bold = True
    p_sub.font.color.rgb = SECONDARY

    exceptions = [
        ("EmployeeError / InvalidSalaryError:", "Raised when salaries are negative or mandatory identity fields are missing."),
        ("DuplicateAttendanceError:", "Prevents recording multiple attendance entries for the same employee on the same date."),
        ("DuplicatePayrollError:", "Guarantees payroll cannot be generated twice for the same employee and calendar month."),
        ("PayrollNotFinalizedError:", "Disallows recording a disbursement payment before payroll has been formally reviewed and finalized."),
        ("Graceful GUI Integration:", "All exceptions are intercepted and displayed as clear user-friendly messagebox popups.")
    ]
    for t, d in exceptions:
        p = tf7_r.add_paragraph()
        p.text = f"✔ {t} "
        p.font.bold = True
        p.font.size = Pt(12)
        p.font.color.rgb = DARK_TEXT
        r = p.add_run()
        r.text = d
        r.font.bold = False
        r.font.color.rgb = MUTED_TEXT

    # ==========================================
    # SLIDE 8: TKINTER GUI WALKTHROUGH
    # ==========================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "Desktop User Interface (Tkinter / ttk)", "User Interface & Experience")

    gui_tabs = [
        ("1. Dashboard", "Live KPI cards: active headcount, monthly total payroll, pending & completed payments."),
        ("2. Employee Mgmt", "Form with validation + Treeview directory; search by ID/Name, add, update, safe delete."),
        ("3. Attendance Mgmt", "Check-in/out logging, auto working hour computation, overtime calculation, date filtering."),
        ("4. Leave Mgmt", "Apply for paid/unpaid leaves, approval & rejection controls, multi-day span calculations."),
        ("5. Compensation", "Custom allowances (HRA, transport, medical), performance bonuses, and extra deductions."),
        ("6. Payroll Processing", "Monthly batch payroll generation, draft breakdown viewer, and finalization lock."),
        ("7. Payslips", "Mono-spaced formatted payslip preview and instant export to .txt file in payslips/."),
        ("8. Payment History", "Disbursement simulation: mark pending payrolls as Paid via UPI, Bank, Cash, or Cheque.")
    ]

    tab_coords = [
        (Inches(0.8), Inches(1.6)), (Inches(3.8), Inches(1.6)), (Inches(6.8), Inches(1.6)), (Inches(9.8), Inches(1.6)),
        (Inches(0.8), Inches(4.3)), (Inches(3.8), Inches(4.3)), (Inches(6.8), Inches(4.3)), (Inches(9.8), Inches(4.3))
    ]

    for idx, (t_name, t_desc) in enumerate(gui_tabs):
        x, y = tab_coords[idx]
        add_card(s8, x, y, Inches(2.75), Inches(2.5))
        tb = s8.shapes.add_textbox(x + Inches(0.15), y + Inches(0.2), Inches(2.45), Inches(2.1))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = t_name
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = PRIMARY
        
        p_desc = tf.add_paragraph()
        p_desc.text = t_desc
        p_desc.font.size = Pt(11)
        p_desc.font.color.rgb = DARK_TEXT

    # ==========================================
    # SLIDE 9: TESTING & DEMONSTRATION SCENARIOS
    # ==========================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "Sample Test Scenarios & Automated Unit Testing", "Verification & Quality")

    # Left: 4 Sample Employees (Demonstration Data)
    add_card(s9, Inches(0.8), Inches(1.6), Inches(6.8), Inches(5.2))
    b_demo = s9.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(6.4), Inches(4.8))
    tf9_l = b_demo.text_frame
    tf9_l.word_wrap = True
    
    p = tf9_l.paragraphs[0]
    p.text = "Four Sample Scenarios (October 2026)"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = PRIMARY
    
    demos = [
        ("EMP001 - Rahul Sharma (Salaried, Rs. 50k)", "Full 22 days attendance + 4 overtime hours + HRA/Transport allowances."),
        ("EMP002 - Priya Patel (Salaried, Rs. 60k)", "18 present, 2 paid leaves, 1 unpaid leave (deducted), 1 absent (deducted) + Rs. 5k bonus."),
        ("EMP003 - Amit Kumar (Hourly, Rs. 300/hr)", "Clocked 20 days (including 10 overtime hours) + 2 absent days. Pay calculated strictly from hours."),
        ("EMP004 - Neha Singh (Hourly, Rs. 250/hr)", "17 regular days, 2 half-days (4h each), 1 absent, 2 holidays + Rs. 500 deduction.")
    ]
    for name, desc in demos:
        p = tf9_l.add_paragraph()
        p.text = f"▶ {name}"
        p.font.bold = True
        p.font.size = Pt(12)
        p.font.color.rgb = SECONDARY
        p_d = tf9_l.add_paragraph()
        p_d.text = desc
        p_d.font.size = Pt(11)
        p_d.font.color.rgb = DARK_TEXT

    # Right: Unit Test Suite
    add_card(s9, Inches(8.0), Inches(1.6), Inches(4.5), Inches(5.2))
    b_test = s9.shapes.add_textbox(Inches(8.2), Inches(1.8), Inches(4.1), Inches(4.8))
    tf9_r = b_test.text_frame
    tf9_r.word_wrap = True
    
    p = tf9_r.paragraphs[0]
    p.text = "Automated Unit Tests"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = ACCENT

    test_stats = [
        ("Test Suite:", "30 Unit Tests (test_payroll.py)"),
        ("Pass Rate:", "100% Passing (0 Failures, 0 Errors)"),
        ("Execution Time:", "< 1.0 second"),
        ("Coverage Areas:", "• Salaried & Hourly calculation\n• Overtime & deduction math\n• Working hours computation\n• Duplicate payroll prevention\n• Finalization before payment lock\n• Isolated temp file JSON CRUD\n• Text payslip export validation")
    ]
    for l, val in test_stats:
        p = tf9_r.add_paragraph()
        p.text = f"{l} "
        p.font.bold = True
        p.font.size = Pt(12)
        p.font.color.rgb = DARK_TEXT
        r = p.add_run()
        r.text = val
        r.font.bold = False
        r.font.color.rgb = MUTED_TEXT

    # ==========================================
    # SLIDE 10: CONCLUSION & VIVA HIGHLIGHTS
    # ==========================================
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "Conclusion & Key Viva Presentation Takeaways", "Summary & Evaluation")

    viva_cards = [
        ("1. Pure Standard Python", "No external dependencies, web bloat, or complex SQL setup. Runs out of the box on any Python 3 environment.", Inches(0.8), Inches(1.6)),
        ("2. Meaningful OOP", "Concepts are not forced; inheritance, polymorphism, and composition emerge naturally from the business domain.", Inches(6.9), Inches(1.6)),
        ("3. High Explainability", "Every class has a distinct single responsibility. Every team member can confidently walk an examiner through the code.", Inches(0.8), Inches(3.6)),
        ("4. Resilient Persistence", "JSON records retain all state across restarts. Finalization locks protect historical payroll records against accidental changes.", Inches(6.9), Inches(3.6))
    ]

    for title, desc, x, y in viva_cards:
        add_card(s10, x, y, Inches(5.6), Inches(1.6))
        tb = s10.shapes.add_textbox(x + Inches(0.2), y + Inches(0.15), Inches(5.2), Inches(1.3))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = PRIMARY
        p_d = tf.add_paragraph()
        p_d.text = desc
        p_d.font.size = Pt(11)
        p_d.font.color.rgb = DARK_TEXT

    # Bottom Banner: How to Run
    add_card(s10, Inches(0.8), Inches(5.5), Inches(11.7), Inches(1.3), bg_color=PRIMARY, border_color=None)
    b_run = s10.shapes.add_textbox(Inches(1.0), Inches(5.6), Inches(11.3), Inches(1.1))
    tf10 = b_run.text_frame
    tf10.word_wrap = True
    p = tf10.paragraphs[0]
    p.text = "READY FOR DEMONSTRATION & VIVA EVALUATION"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = RGBColor(147, 197, 253)
    p2 = tf10.add_paragraph()
    p2.text = "Launch GUI:  python main.py       |       Run Unit Tests:  python -m unittest tests/test_payroll.py"
    p2.font.size = Pt(14)
    p2.font.bold = True
    p2.font.color.rgb = RGBColor(255, 255, 255)

    # Save Presentation
    output_path = os.path.join(os.getcwd(), "Payroll_System_OOP_Presentation.pptx")
    prs.save(output_path)
    print(f"Presentation saved successfully at: {output_path}")

if __name__ == "__main__":
    create_deck()
