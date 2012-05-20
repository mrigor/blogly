from django.core.paginator import Paginator

class Page(Paginator):

  def __init__(self, *args, **kwargs):
        super(Page, self).__init__(*args, **kwargs)

  def getPages(self, current, pagesDisplayed=10):
    """
    Gets a list of page numbers which should be displayed to the user.
    """
    numPages = self.num_pages
    if numPages <= pagesDisplayed:
      return range(1, numPages + 1)

    if current < pagesDisplayed / 2:
      return range(1, pagesDisplayed + 1)

    if current >= (numPages - (pagesDisplayed / 2)):
      return range(numPages - (pagesDisplayed - 1), numPages + 1)

    return range(current - (pagesDisplayed / 2) + 1,
                 current + (pagesDisplayed / 2) + 1)
