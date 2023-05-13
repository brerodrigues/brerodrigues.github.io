# brenn0_weblog

Theme used is [**Jekyll Shell Theme**](https://github.com/tareqdandachi/jekyll-shell-theme) with some modifications:
- Created a _posts folder for blog posts.
- Created a _posts/post.html layout capable of showing the read time of a post.
- Inserted in the _includes/footer.html of includes the date of a post (showed only when a page is a blog post) and the twitter handle.
- Modified the `<p>` html tag to `text-align: justify` in assets/css/main.scss
- Inserted the plugin `jekyll-feed`
- Inserted posts tags in the post
- Inserted the tag_page.html in _layouts folder to show posts by tags
- Inserted update_tags.py script to generate .md tags in the tags folder because in githubpages we cannot generate them
  - Warning: this script is modified by me and the modificiations are not well documented for now

Feel free to create your fork and modify too.
