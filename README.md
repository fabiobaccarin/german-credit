# German credit data science case study

This repository implements a case study in data science using the
[German credit dataset] ([OpenML] ID: 31).

## About the repository

This repository adheres to a few conventions and guidelines:

1. **Specification-driven development.** Every functionality is implemented
   first as a [Markdown] file inside the `specs/` directory. Each Markdown file
   is named after the corresponding [Python] file implementing the functionality
   inside `src/german_credit/`. For example, `specs/data.md` refers to the
   `src/german_credit/data.py` file.
2. **Design by contract.** Every functionality is implemented using the
   [Design By Contract] philosophy. Every function must implement a set of
   requirements (preconditions), assurances (postconditions) and guarantees
   (invariants). Such elements are described in the approriate specification
   file.
3. **Google style.** All files implement Google's style conventions. In
   particular, we follow the [Google Markdown style guide] and the
   [Google Python style guide].
4. **Index files.** We call Markdown files used as entrypoints to other Markdown
   files as *index files*. The are creatively named `index.md`. There are 2
   index files in the project:
   1. `german_credit/index.md`: this file contains structions for AI to generate
      code for the project.
   2. `specs/index.md`: this file is the entrypoint for the project's
      specifications, containing an overview of functionality implemented in
      code

[German credit dataset]: https://www.openml.org/d/31
[OpenML]: https://www.openml.org/
[Markdown]: https://www.markdownguide.org/
[Python]: https://www.python.org/
[Google Markdown style guide]: https://google.github.io/styleguide/docguide/style.html
[Google Python style guide]: https://google.github.io/styleguide/pyguide.html
