from django.core.paginator import InvalidPage, EmptyPage

from common.paging import Page
from comments.models import Comment
from util.utils import OrderedDict

class MissingRequiredParameters(Exception):
    pass

def get_comments_order_by(type):
    if type == '-chronological':
        return 'reverse_thread_id'
    return 'thread_id' # default for 'chronological' type

def get_comments_page(request, rpp=10, order_by='chronological', type=None, obj=None):
    if not obj or not type:
      raise MissingRequiredParameters('Missing "obj" or "type" parameters.')
    order_by = get_comments_order_by(order_by)
    comments_list = Comment.objects.filter(thing_id=obj.id, type=type) \
        .order_by(order_by).all()

    comments = Page(comments_list, rpp)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        comments = comments.page(page)
    except (EmptyPage, InvalidPage):
        comments = comments.page(comments.num_pages)

    comments_list = comments.object_list


    def get_children(comments, id, skip=[]):
        children = OrderedDict((obj, comments[obj]) \
            for obj in comments \
            if (comments[obj].parent_id == id and comments[obj].id not in skip))

        #print 'children', children
        out = OrderedDict()
        for child in children:
            #print 'sub child', child
            #print 'get_children', get_children(comments, child)
            if child in comments:
                del comments[child]
            skip.append(child)
            #print 'comments', comments
            #print 'skip', skip
            out[child] = get_children(comments, child, skip)
        return out


    cs = list(comments_list)

    #make a tree
    comment_tree = OrderedDict()
    comment_index = OrderedDict((obj.id, obj) for obj in comments_list)
    skip = []
    for index in comment_index:
        if index not in skip:
            cm = comment_index[index]
            print 'get children for ', cm.id
            comment_tree[cm.id] = get_children(comment_index.copy(), cm.id, skip)
    print 'comments'
    print comments
    print 'tree'
    print comment_tree
    return comments, comment_index, comment_tree


def get_thread_id(type, thing_id, parent=None):
    '''
    Used to get thread_id / reverse_thread_id for comment sorting
    '''
    if parent:
        # reply
        return (parent.thread_id + '.'  + ("%06d" % 0), parent.reverse_thread_id + '.' + ("%06d" % 0))
    else:
        # handle new comments
        # get last comment
        comments = Comment.objects \
                .filter(type=type, thing_id=thing_id, parent_id=None) \
                .order_by('-thread_id') \
                .all()[:1]
        if not len(comments):
            return ('000000', '999999')
        last_thread_id = comments[0].thread_id
        last_reverse_thread_id = comments[0].reverse_thread_id
        return ("%06d" % (int(last_thread_id) + 1), str((int(last_reverse_thread_id) - 1)))
