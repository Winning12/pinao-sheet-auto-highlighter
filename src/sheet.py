from src.tools import *
from src.line import Line
from src.constants import *

class Sheet:

    width = None

    height = None

    top_left = None

    image = None

    lines = []

    line_height = None

    line_gap = 0

    def __init__(self, image_path, line_height):
        self.image = read(image_path)
        self.width = self.image.shape[::-1][1]
        self.height = self.image.shape[::-1][2]
        self.line_height = line_height
        self.top_left = (0, 0)

        self.construct_lines()

        self.draw_lines()
        self.draw_sheet()
        self.draw_bars()

    def construct_lines(self):
        brace_points = find_all_dir_templates(self.image, brace_dir, 0.85, 5000)
        bar_line_points = find_all_dir_templates(self.image, bar_line_dir, 0.85, 5000)
        sharp_points = find_all_dir_templates(self.image, sharp_dir, 0.75, 10)
        flat_points = find_all_dir_templates(self.image, flat_dir, 0.75, 10)
        natural_points = find_all_dir_templates(self.image, natural_dir, 0.75, 10)


        self.line_gap = int((brace_points[1][1]-brace_points[0][1]-self.line_height)/2)
        for brace_point in brace_points:
            top_left_point = (0, brace_point[1]-self.line_gap)
            line = Line(self.image, top_left_point, self.line_height, self.line_gap, bar_line_points, sharp_points, flat_points, natural_points)
            self.lines.append(line)

    def analyze_sharp_flat_natural(self):
        all_sharp_points = find_all_dir_templates(self.image, sharp_dir, 0.75, 10)
        all_flat_points = find_all_dir_templates(self.image, flat_dir, 0.75, 10)
        all_natural_points = find_all_dir_templates(self.image, natural_dir, 0.75, 10)
        for line in self.lines:
            line.analyze_sharp_and_flat_points(all_sharp_points, all_flat_points, all_natural_points)

    # visualize sheet components
    def draw_sheet(self):
        draw_one_rectangle(self.image, (0, 0), self.width, self.height, blue)

    def draw_lines(self):
        for line in self.lines:
            line.draw_line()

    def draw_bars(self):
        for line in self.lines:
            line.draw_bars()

    def save(self, name):
        save(name, self.image)