## Javascript demo

This subdirectory contains the code for the javascript demo of the
Multiplicative Weights Update Algorithm. You can try it out [here](j2kun.github.io/mwua/index.html).

### Building from scratch

Prerequisites: `node`, `gulp`

I was flexing some software muscles when making this project, so it's written
in ECMA 6 (the "modern" update to Javascript), and compiled to
browser-renderable Javascript using browserify with a bunch of plugins.

I used `yarn` as the package manager, but you can also build using `npm`.

Setup:

```
npm install -g yarn  # only if you don't have yarn
yarn install --dev
gulp build  # or gulp watch
open index.html
```


