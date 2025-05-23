import traceback

from tasks.base.assets.assets_base_page import *


class Page:
    # Key: str, page name like "page_main"
    # Value: Page, page instance
    all_pages = {}

    @classmethod
    def clear_connection(cls):
        for page in cls.all_pages.values():
            page.parent = None

    @classmethod
    def init_connection(cls, destination):
        """
        Initialize an A* path finding among pages.

        Args:
            destination (Page):
        """
        cls.clear_connection()

        visited = [destination]
        visited = set(visited)
        while 1:
            new = visited.copy()
            for page in visited:
                for link in cls.iter_pages():
                    if link in visited:
                        continue
                    if page in link.links:
                        link.parent = page
                        new.add(link)
            if len(new) == len(visited):
                break
            visited = new

    @classmethod
    def iter_pages(cls):
        return cls.all_pages.values()

    @classmethod
    def iter_check_buttons(cls):
        for page in cls.all_pages.values():
            yield page.check_button

    def __init__(self, check_button):
        self.check_button = check_button
        self.links = {}
        (filename, line_number, function_name, text) = traceback.extract_stack()[-2]
        self.name = text[:text.find('=')].strip()
        self.parent = None
        Page.all_pages[self.name] = self

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return self.name

    def link(self, button, destination):
        self.links[destination] = button


# Main page
page_main = Page(MAIN_GOTO_AFFAIRS)

# Adventures
page_adventures = Page(ADVENTURES_CHECK)
page_adventures.link(CLOSE, destination=page_main)
page_main.link(MAIN_GOTO_ADVENTURES, destination=page_adventures)

# Affairs
page_affairs = Page(AFFAIRS_GOTO_DEPTHS)
page_affairs.link(CLOSE, destination=page_main)
page_main.link(MAIN_GOTO_AFFAIRS, destination=page_affairs)

# Dashboard
page_dashboard = Page(DASHBOARD_CHECK)
page_dashboard.link(CLOSE, destination=page_main)
page_main.link(MAIN_GOTO_DASHBOARD, destination=page_dashboard)

# Depths
page_depths = Page(DEPTHS_CHECK)
page_depths.link(CLOSE, destination=page_main)
page_affairs.link(AFFAIRS_GOTO_DEPTHS, destination=page_depths)

# Balloon
page_balloon = Page(BALLOON_CHECK)
page_balloon.link(CLOSE, destination=page_main)
page_affairs.link(AFFAIRS_GOTO_BALLOON, destination=page_depths)

# Pavilion
page_pavilion = Page(PAVILION_CHECK)
page_pavilion.link(CLOSE, destination=page_main)
page_affairs.link(AFFAIRS_GOTO_PAVILION, destination=page_depths)

# Shop
page_shop = Page(SHOP_CHECK)
page_shop.link(CLOSE, destination=page_main)
page_main.link(MAIN_GOTO_SHOP, destination=page_shop)

# Gacha
page_gacha = Page(GACHA_CHECK)
page_gacha.link(CLOSE, destination=page_main)
page_main.link(MAIN_GOTO_GACHA, destination=page_gacha)