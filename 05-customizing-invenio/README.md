# Tutorial 05 - Customizing the look & feel

In this session we will customize minor visual elements of our Invenio
instance, like the logo of our instance, the colors and fonts, the way search
results for records are displayed and the display page for every record.

## Table of Contents

- [Table of Contents](#table-of-contents)
- [Step 1: Run the development server](#step-1-run-the-development-server)
- [Step 2: Change the frontpage titles](#step-2-change-the-frontpage-titles)
- [Step 3: Change the site logo](#step-3-change-the-site-logo)
- [Step 4: Change the theming](#step-4-change-the-theming)
- [Step 5: Change how record search results are displayed](#step-5-change-how-record-search-results-are-displayed)
- [Step 6: Change the record page](#step-6-change-the-record-page)

## Step 1: Run the development server

If your development server is not running you can run:

```bash
cd ~/src/my-site
docker-compose up -d
./scripts/server
```

## Step 2: Change the frontpage titles

Although the default look of the instance looks fine, we can do better! Let's
start small by changing some text on the frontpage. To do so we have to edit
`my_site/config.py`:

```diff
# Theme configuration
# ===================
#: Site name
THEME_SITENAME = _('My site')
#: Use default frontpage.
THEME_FRONTPAGE = True
#: Frontpage title.
-THEME_FRONTPAGE_TITLE = _('My site')
+THEME_FRONTPAGE_TITLE = _('The coolest repository!')
#: Frontpage template.
THEME_FRONTPAGE_TEMPLATE = 'my_site/frontpage.html'
```

Let's also change the "Welcome to My site." text to something motivational, by
editing `my_site/theme/templates/semantic-ui/my_site/frontpage.html`:

```diff
{%- extends "invenio_theme/frontpage.html" %}

{%- block page_body %}
<div class="container marketing">
  <div class="row">
    <div class="col-lg-12">
-   <h1 class="text-center">Welcome to My site.</h1>
+   <h1 class="text-center">Get educated!</h1>
  </div>
</div>
{%- endblock %}
```

If you now go to <https://127.0.0.1:5000/> you will see the changed titles:

![Invenio front page](./images/frontpage-title.png)

## Step 3: Change the site logo

Our instance is powered by Invenio, but not defined by it! Let's change the
logo to something else. First we have to add the actual image of our new logo
inside a folder that our application will know it's part of its assets:

```bash
# Create the "static/images" folder inside the "my_site/theme" directory
$ mkdir -p my_site/theme/static/images
# Copy the provided logo from
$ cp ~/src/training/05-customizing-invenio/extras/my-site-logo.png my_site/theme/static/images/
# We have to tell the application to "collect" the new static file
$ invenio collect -v
Collect static from blueprints.
Copied: [my_site] '/home/bootcamp/.local/share/virtualenvs/my-site-7Oi5HgLM/var/instance/static/images/my-site-logo.png'
```

We also have to override the `THEME_LOGO` configuration variable, by adding it
in `my_site/config.py`:

```diff
# Theme configuration
# ===================
#: Site name
THEME_SITENAME = _('My site')
#: Use default frontpage.
THEME_FRONTPAGE = True
#: Frontpage title.
THEME_FRONTPAGE_TITLE = _('The coolest repository!')
#: Frontpage template.
THEME_FRONTPAGE_TEMPLATE = 'my_site/frontpage.html'
+#: Theme logo.
+THEME_LOGO = 'images/my-site-logo.png'
```

If you reload the page you will see the new logo on the top left:

![Invenio front page logo](./images/frontpage-logo.png)

## Step 4: Change the theming

Until this moment, we've basically performed "content" changes. In order to
modify the "style" of the site we have to make changes to the produced CSS.

Invenio uses LESS in order define CSS styles in a flexible and extensible way.
The `.less` we are interested in changing is
`my_site/theme/assets/semantic-ui/less/my_site/site/globals/site.variables`:

```diff
// If you want to change the brand color you can do something like:
-// @brandColor      : #793e8e;
+@brandColor      : #793e8e;
```

If we want to be more precise and change a concrete CSS rule we can add it directly in `my_site/theme/assets/semantic-ui/less/my_site/site/globals/site.overrides`

```diff
/* Provide here your custom css */

-// footer{
-//    margin-top: 3px;
-//  }
-//
-//  html.cover-page{
-//    background-color: rgb(226, 147, 43);
-//  }
-//
-//  .content{
-//    .header{
-//        font-size: xx-large !important;
-//      }
-//  }
+ footer{
+    margin-top: 3px;
+  }
+
+  html.cover-page{
+    background-color: rgb(226, 147, 43);
+  }
+
+  .content{
+    .header{
+        font-size: xx-large !important;
+      }
+  }
```

After changing the file, we have to rebuild our assets using the `invenio
webpack` command:

```console
(my-site) $ invenio webpack buildall
...webpack
```

If we reload our page now we should see our brand new design:

![Invenio front page with purple background](./images/frontpage-color.png)

You can watch for changes and automatically rebuild the assets by running:

```console
(my-site) $ invenio webpack run start
```

## Step 5: Change how record search results are displayed

If you navigate to the search results page (<https://localhost:5000/search>)
you can see the following:

![Search page result list](./images/search-old.png)

Let's change the way the title and authors of each result look like. The
current search UI application is built with React. In our case we'll have to
modify the `MysiteResultsListItem` component from `my_site/theme/assets/semantic-ui/templates/search/ResultsList.item.jsx`:

```diff
export const MysiteResultsListItem = ({ result, index }) => {
  const contributors = result.metadata.contributors || [];
  return (
    <Item key={index} href={`/records/${result.id}`}>
      <Item.Content>
        <Item.Header>{result.metadata.title}</Item.Header>
        <Item.Description>
+         <p><b>Authors</b></p>
          {contributors && (
            <List horizontal relaxed>
              {contributors.map((contributor, idx) => (
                <List.Item key={idx}>{contributor.name}</List.Item>
              ))}
            </List>
          )}
        </Item.Description>
      </Item.Content>
    </Item>
  );
};
```

Again, we'll have to run the `invenio webpack buildall` command:

```bash
(my-site) $ invenio webpack buildall
...webpack
```

And now, if we refresh we'll see that our search results display differently:

![Invenio page result list with strong and emphasis styles](./images/search-new.png)

If we want to change the grid layout display we'll have to modify the `MysiteResultsGridItem` component from `my_site/theme/assets/semantic-ui/templates/search/ResultsGrid.item.jsx`:

```diff
export const MysiteResultsGridItem = ({ result, index }) => {
  const contributors = result.metadata.contributors || [];
  return (
    <Card fluid key={index} href={`/records/${result.id}`}>
      <Card.Content>
-       <Card.Header>{result.metadata.title}</Card.Header>
+       <Card.Header textAlign="center">{result.metadata.title}</Card.Header>
        <Card.Description>
          {contributors && (
            <List horizontal relaxed>
              {contributors.map((contributor, idx) => (
                <List.Item key={idx}>{contributor.name}</List.Item>
              ))}
            </List>
          )}
        </Card.Description>
      </Card.Content>
    </Card>
  );
};
```

Again, we'll have to run the `invenio webpack buildall` command:

```console
(my-site) $ invenio webpack buildall
...webpack
```

And now, if we refresh we'll see that our grid search results display differently:

![Invenio page result grid with title centered](./images/search-grid-modified.png)

Side note: The components that we just modified are overwriting components from `invenio-search-ui`. More information on how to do it [here](https://github.com/inveniosoftware/invenio-search-ui/blob/master/docs/customizing.rst).

## Step 6: Change the record page

If you actually click on one of the search results you will be redirected to
the record's page:

![Record details page](./images/record-old.png)

To change this view we'll have to modify the Jinja template that renders the
page, `my_site/records/templates/semantic-ui/records/record.html`. Let's do something
similar to what we did with the search results:

```diff
{%- block page_body %}
<div class="container">
  <h2>{{record.title}}</h2>
- <div class="panel panel-default">
-   <ul class="list-group">
-     {{ record_content(record) }}
-   </ul>
- </div>
+ <strong>Authors</strong>
+ {% for author in record.contributors %}
+ <em>{{ author.name }}</em>;
+ {% endfor %}
</div>
{%- endblock %}
```

If you refresh the record's page you'll see something like this:

![Record details page with styles](./images/record-new.png)
