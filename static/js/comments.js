GB['comments'] = {
  'reply': function(e, type){
    e.preventDefault();
    var self = this;
    var button = jq(e.target);
    this.parent = button.closest('div.comment');
    this.parent_id = self.parent.attr('id').split('_')[1];
    this.url = '/remote/' + type + '/comment/' + this.parent_id + '/reply/';
    var form = self.parent.data('form')
    if(!form){
      form = jq([
          '<div class="replyContainer">',
          '<form method=post action="">',
          '<textarea name="content"></textarea>',
          '<div>',
          '<input class="btn btn-mini" type="submit" value="Submit"/>',
          '</div>',
          '</form>',
          '<div',
      ].join('')).css({'display': 'none'}).appendTo(self.parent);
      self.openForm(form);
      self.parent.data('form', form);
    }else{
      if(form.height()){
        self.closeForm(form);
      }else{
        self.openForm(form);
      }

    }
    jq(form).find('form').unbind('submit').bind('submit', function(e){
          e.preventDefault();
          self.handleSubmit.call(self, this);
    });
  },
  'edit': function(e, type){
    e.preventDefault();
    var self = this;
    var button = jq(e.target);
    this.parent = button.closest('div.comment');
    this.comment_id = self.parent.attr('id').split('_')[1];
    this.url = '/remote/' + type + '/comment/' + this.comment_id + '/edit/';
    console.log('create form');
    form = jq([
        '<div class="replyContainer">',
        '<form method=post action="">',
        '<textarea name="content"></textarea>',
        '<div>',
        '<input class="btn btn-mini" type="submit" value="Save"/>',
        '</div>',
        '</form>',
        '<div',
    ].join('')).css({'display': 'none'});
    self.parent.after(form);
    console.log(self.parent);
    console.log('hide parent');
    self.parent.hide();
    self.populateForm(form, this.parent);
    self.openForm(form);
    console.log('toggle form');
    if(form.height()){
      self.closeForm(form);
    }else{
      self.openForm(form);
    }
    jq(form).find('form').unbind('submit').bind('submit', function(e){
          e.preventDefault();
          self.handleSubmit.call(self, this);
    });
  }
};
GB.comments.reply.prototype = {
  handleSubmit: function(form){
    var self = this;
    form = jq(form);
    console.log(self, self.parent_id);
    jq.post(this.url, {
        'content': form.find('textarea').val(),
        'parent_id': self.parent_id
    }, function(response){
      console.log(1);
      console.log(response);
      self.closeForm(form);
      console.log(self.parent);
      if('content' in response){
        var childrenContainer = self.parent.find('children');
        if(!childrenContainer.length){
          childrenContainer = jq('<ul class="children"/>').appendTo(self.parent);
        }
        childrenContainer.append(jq(response.content));
      }
    }, 'json');
  },
  openForm: function(form){
    console.log('open');
    form.css({'height': 'auto', 'left': '-10000px', 'position': 'absolute', 'display': 'block'});
    var height = form.height();
    form.css({'position': 'static', 'overflow':'hidden', 'height': 0}).animate({
        'height': height
    }, 300, function(){
      jq(this).css({'height': 'auto'});
    });
  },
  closeForm: function(form){
    console.log('close', form);
    form.animate({'height': 0}, 300);
  }
};

GB.comments.edit.prototype = {
  handleSubmit: function(form){
    var self = this;
    form = jq(form);
    console.log(self, self.comment_id);
    jq.post(this.url, {
        'content': form.find('textarea').val(),
        'comment_id': self.comment_id
    }, function(response){
      console.log(response);
      form.remove();
      //self.closeForm(form);
      console.log(self.parent);
      if('content' in response){
        console.log(response);
        self.parent.find('.content').html(response.content);
        self.parent.show();
      }
    }, 'json');
  },
  openForm: GB.comments.reply.prototype.openForm,
  closeForm: GB.comments.reply.prototype.closeForm,
  populateForm: function(form, commentContainer){
    var textarea = form.find('textarea');
    var content = commentContainer.find('.content').html();
    textarea.val(content);
  }
};
