## Javascript demo

This subdirectory contains the code for the javascript demo of the
Multiplicative Weights Update Algorithm. You can try it out [here]().

### Building from scratch

I was flexing some software muscles when making this project, so it's written
in ECMA 6 (the "modern" update to Javascript), and compiled to
browser-renderable Javascript using babel.

I used `yarn` as the package manager, but you can also build using `npm`.

Setup:

```
npm install -g yarn  # only if you don't have yarn
yarn install --dev
yarn run babel
open index.html
```


