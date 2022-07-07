#!/usr/bin/python3
"""Main file for the GUI."""
import gettext
from uuid import uuid1

# import dbus
from PySide6 import QtCore, QtWidgets, QtGui

import database


# TODO Configure it to use the "/usr/share/locale" directory.
gettext.bindtextdomain("moadaly", "locale")
gettext.textdomain("moadaly")
_ = gettext.gettext


class MainWindow(QtWidgets.QMainWindow):
    """Main window."""

    def __init__(self):
        """Initialize main components of the window."""
        super().__init__()

        self.setMinimumSize(1000, 700)
        self.setWindowTitle(_("Moadaly"))

        main_window_layout = QtWidgets.QVBoxLayout()

        top_panel_layout = QtWidgets.QHBoxLayout()
        bottom_panel_layout = QtWidgets.QVBoxLayout()

        # Create main window widgets.
        self.result_box = ResultBox()
        self.previous_gpa_box = PreviousGPABox()
        self.calculation_system_box = CalculationSystemBox()
        self.grades_panel = GradesPanel()

        # Add main components to the main window layout.
        top_panel_layout.addWidget(self.result_box)
        top_panel_layout.addWidget(self.previous_gpa_box)
        top_panel_layout.addWidget(self.calculation_system_box)
        bottom_panel_layout.addWidget(self.grades_panel.scroll_area)

        main_window_layout.addLayout(top_panel_layout)
        main_window_layout.addLayout(bottom_panel_layout)

        central_widget = QtWidgets.QWidget()
        central_widget.setLayout(main_window_layout)

        self.setCentralWidget(central_widget)


class ResultBox(QtWidgets.QWidget):
    """A Group Box where the results are displayed, such as, GPA, grade, total hours and points."""

    def __init__(self):
        """Initialize components of the results widget."""
        super().__init__()

        group_box = QtWidgets.QGroupBox(_("Result"))
        group_box.setParent(self)

        # TODO Use QFormLayout
        group_box_layout = QtWidgets.QGridLayout()

        # Result GPA.
        group_box_layout.addWidget(QtWidgets.QLabel(_("GPA:")), 0, 0)
        self.result_gpa = QtWidgets.QLabel(_("Undefined"))
        self.result_gpa.setStyleSheet(
            """
        font: bold;
        """
        )
        group_box_layout.addWidget(self.result_gpa, 0, 1)

        # Result hours.
        group_box_layout.addWidget(QtWidgets.QLabel(_("Hours:")), 1, 0)
        self.result_hours = QtWidgets.QLabel("0")
        self.result_hours.setStyleSheet(
            """
        font: bold;
        """
        )
        group_box_layout.addWidget(self.result_hours, 1, 1)

        # Result points.
        group_box_layout.addWidget(QtWidgets.QLabel(_("Points:")), 2, 0)
        self.result_points = QtWidgets.QLabel("0.00")
        self.result_points.setStyleSheet(
            """
        font: bold;
        """
        )
        group_box_layout.addWidget(self.result_points, 2, 1)

        # Result grade.
        group_box_layout.addWidget(QtWidgets.QLabel(_("Grade:")), 3, 0)
        self.result_grade = QtWidgets.QLabel(_("Undefined"))
        self.result_grade.setStyleSheet(
            """
        font: bold;
        """
        )
        group_box_layout.addWidget(self.result_grade, 3, 1)

        group_box.setLayout(group_box_layout)


class PreviousGPABox(QtWidgets.QWidget):
    """A Group Box where you can specify a previous GPA, to add it to the calculation."""

    def __init__(self):
        """Initialize components of the previous GPA widget."""
        super().__init__()

        group_box = QtWidgets.QGroupBox(_("Previous GPA"))
        group_box.setParent(self)

        # TODO Use QFormLayout
        group_box_layout = QtWidgets.QGridLayout()

        # Previous Hours.
        group_box_layout.addWidget(QtWidgets.QLabel(_("Previous Hours:")), 0, 0)
        self.previous_hours = QtWidgets.QLineEdit()
        self.previous_hours.setValidator(QtGui.QIntValidator(bottom=0))
        group_box_layout.addWidget(self.previous_hours, 0, 1)

        # Previous GPA.
        group_box_layout.addWidget(QtWidgets.QLabel(_("Previous GPA:")), 1, 0)
        self.previous_gpa = QtWidgets.QLineEdit()
        # TODO Set the maximum value to 4 or 5 for the GPA depending on the used GPA system.
        self.previous_gpa.setValidator(QtGui.QDoubleValidator(bottom=0))
        group_box_layout.addWidget(self.previous_gpa, 1, 1)

        group_box.setLayout(group_box_layout)


class CalculationSystemBox(QtWidgets.QWidget):
    """A Group Box where you can specify the GPA calculation system."""

    def __init__(self):
        """Initialize components of the calculation system widget."""
        super().__init__()

        main_group_box = QtWidgets.QGroupBox(_("Calculation System"))
        main_group_box.setParent(self)

        group_box_layout = QtWidgets.QHBoxLayout()

        group_box_layout.addWidget(self.init_point_scale_box())
        group_box_layout.addWidget(self.init_grading_system_box())

        main_group_box.setLayout(group_box_layout)

    def init_point_scale_box(self) -> QtWidgets.QGroupBox:
        """Create point scale setting box."""
        point_scale_group_box = QtWidgets.QGroupBox(_("Point Scale"))
        point_scale_group_box_layout = QtWidgets.QVBoxLayout()

        radio_five_system = QtWidgets.QRadioButton("5.000")
        radio_five_system.setChecked(True)
        point_scale_group_box_layout.addWidget(radio_five_system)

        radio_four_system = QtWidgets.QRadioButton("4.000")
        point_scale_group_box_layout.addWidget(radio_four_system)
        # TODO Enable the option when the 4 point scale system is implemented.
        radio_four_system.setDisabled(True)

        point_scale_group_box.setLayout(point_scale_group_box_layout)

        return point_scale_group_box

    def init_grading_system_box(self) -> QtWidgets.QGroupBox:
        """Create grading system setting box."""
        point_scale_group_box = QtWidgets.QGroupBox(_("Grading System"))
        point_scale_group_box_layout = QtWidgets.QVBoxLayout()

        radio_normal_system = QtWidgets.QRadioButton(_("Normal"))
        radio_normal_system.setChecked(True)
        point_scale_group_box_layout.addWidget(radio_normal_system)

        radio_curve_system = QtWidgets.QRadioButton(_("Curve"))
        point_scale_group_box_layout.addWidget(radio_curve_system)
        # TODO Enable the option when the curve grading system is implemented.
        radio_curve_system.setDisabled(True)

        point_scale_group_box.setLayout(point_scale_group_box_layout)

        return point_scale_group_box


class GradesPanel(QtWidgets.QWidget):
    """A panel to display semesters, and to handle the addition of new semesters."""

    def __init__(self):
        """Initialize base components of the panel."""
        super().__init__()

        self.semesters = []

        self.layout = QtWidgets.QVBoxLayout(self)

        self.scroll_area = QtWidgets.QScrollArea()

        add_semester_button = QtWidgets.QPushButton(
            QtGui.QIcon().fromTheme("list-add"), _("New Semester")
        )
        add_semester_button.setStyleSheet("background-color: green;")
        add_semester_button.setFixedWidth(200)
        add_semester_button.clicked.connect(self.add_new_semester)
        self.layout.addWidget(add_semester_button, alignment=QtCore.Qt.AlignCenter)

        self.scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scroll_area.setWidgetResizable(True)
        # FIXME Scroll area doesn't cover all the available space in the window.
        self.scroll_area.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.scroll_area.setFixedHeight(500)
        self.scroll_area.setWidget(self)

    def add_new_semester(self):
        """Add new semester widget to the grades panel."""
        widget = SemesterWidget(self)
        self.semesters.append(widget)
        self.layout.insertWidget(len(self.semesters) - 1, widget)


class SemesterWidget(QtWidgets.QWidget):
    """A semester that contain a list of corses, to be added to the grades panel."""

    def __init__(self, parent_panel):
        """Initialize a new semester and it's base components."""
        super().__init__()

        self.parent_panel = parent_panel
        self.semester_id = uuid1()
        self.courses = []

        self.layout = QtWidgets.QVBoxLayout(self)

        # Create the semester title bar.
        title_layout = QtWidgets.QHBoxLayout()

        self.title = QtWidgets.QLabel(
            _("Semester %d") % (len(self.parent_panel.semesters) + 1)
        )
        self.title.setStyleSheet(
            """
        font: bold;
        font-size: 25px;
        background-color: green;
        """
        )
        self.title.setFixedHeight(30)
        title_layout.addWidget(self.title)

        delete_semester_button = QtWidgets.QPushButton(
            QtGui.QIcon().fromTheme("delete"), ""
        )
        delete_semester_button.setFixedWidth(80)
        delete_semester_button.clicked.connect(self.delete_semester)
        title_layout.addWidget(delete_semester_button)

        self.layout.addLayout(title_layout)

        # Create the header for the corses.
        headers_layout = QtWidgets.QHBoxLayout()
        for header in [
            QtWidgets.QLabel(_("Title")),
            QtWidgets.QLabel(_("Name")),
            QtWidgets.QLabel(_("Score")),
            QtWidgets.QLabel(_("Hours")),
            QtWidgets.QLabel(_("Grade")),
        ]:
            # FIXME The alignment with the courses components.
            headers_layout.addWidget(header)

        self.layout.addLayout(headers_layout)

        add_course_button = QtWidgets.QPushButton(
            QtGui.QIcon().fromTheme("list-add"), ""
        )
        add_course_button.setStyleSheet("background-color: green;")
        add_course_button.setFixedWidth(80)
        add_course_button.clicked.connect(self.add_new_course)
        self.layout.addWidget(add_course_button)

    def delete_semester(self):
        """Remove a specified semester from the grades panel."""
        semester_index = self.parent_panel.semesters.index(self)
        self.parent_panel.semesters.pop(semester_index)
        self.deleteLater()

        for i in range(semester_index, len(self.parent_panel.semesters)):
            self.parent_panel.semesters[i].title.setText(_("Semester %d") % (i + 1))

    def add_new_course(self):
        """Add new course widget to the semester."""
        widget = CourseWidget(self)
        self.courses.append(widget)
        self.layout.insertWidget(len(self.courses), widget)


class CourseWidget(QtWidgets.QWidget):
    """A course that can be added inside a semester."""

    def __init__(self, parent_semester):
        """Initialize a new course and it's components."""
        super().__init__()

        self.course_id = uuid1()
        self.parent_semester = parent_semester

        self.layout = QtWidgets.QHBoxLayout(self)

        self.title = QtWidgets.QLabel(
            _("Course %d:") % (len(self.parent_semester.courses) + 1)
        )
        self.title.setStyleSheet(
            """
        font-size: 12px;
        """
        )
        self.layout.addWidget(self.title)

        # TODO Add some validation and placeholders.

        self.name = QtWidgets.QLineEdit()
        self.layout.addWidget(self.name)

        self.score = QtWidgets.QLineEdit()
        self.layout.addWidget(self.score)

        self.hours = QtWidgets.QLineEdit()
        self.layout.addWidget(self.hours)

        self.grade = QtWidgets.QComboBox()
        self.grade.addItems(
            [
                _("Undefined"),
                _("A+"),
                _("A"),
                _("B+"),
                _("B"),
                _("C+"),
                _("C"),
                _("D+"),
                _("D"),
                _("F"),
            ]
        )
        self.layout.addWidget(self.grade)

        self.delete_course_button = QtWidgets.QPushButton(
            QtGui.QIcon().fromTheme("delete"), ""
        )
        self.delete_course_button.clicked.connect(self.delete_course)
        self.layout.addWidget(self.delete_course_button)

    def delete_course(self):
        """Remove a specified course from the semester."""
        course_index = self.parent_semester.courses.index(self)
        self.parent_semester.courses.pop(course_index)
        self.deleteLater()

        for i in range(course_index, len(self.parent_semester.courses)):
            self.parent_semester.courses[i].title.setText(_("Course %d") % (i + 1))


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    raise SystemExit(app.exec())
