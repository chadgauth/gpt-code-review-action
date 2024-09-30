# Code Review with AI

Automate code reviews in your pull requests using the power of OpenAI's GPT-4o-mini language model.

## Badges

[![CI/CD Status](https://github.com/chadgauth/code-review-with-openai/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/chadgauth/code-review-with-openai/actions/workflows/ci-cd.yml)
[![Code Coverage](https://codecov.io/gh/chadgauth/code-review-with-openai/branch/main/graph/badge.svg)](https://codecov.io/gh/chadgauth/code-review-with-openai)
[![Dependabot Status](https://flat.badgen.net/dependabot/chadgauth/code-review-with-openai)](https://dependabot.com/)

## Getting Started

### Step 1: Prerequisites

* An OpenAI API key
* A GitHub repository with a `.yml` file in the `.github/workflows` directory

### Step 2: Create a New Workflow File

Create a new file in your `.github/workflows` directory, e.g., `code-review.yml`.

### Step 3: Configure the Workflow

Add the YAML code below to the file and update the `openai-key` input with your OpenAI API key.

```yaml
on: [pull_request]
jobs:
  code-review:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: write
    steps:
      - uses: actions/checkout@v3
      - uses: chadgauth/code-review-with-openai@v2.0
        with:
          openai-key: ${{ secrets.OPENAI_API_KEY }}
          # Optional inputs:
          # model: 'gpt-4o-mini'
          # max-length: 450000
          # prompt: 'Only suggest performance improvements for this code.'
          # post-if-error: false
          # github-token: ${{ github.token }}
          # excluded_files: |
          #   vendor/**
          #   node_modules/**
          #   *.min.js
```

## Configuration Options

### Required Inputs

* `openai-key`: Your OpenAI API key used for authentication.

### Optional Inputs

* `github-token`: The token used to authenticate with the GitHub API (defaults to `${{ github.token }}`).
* `model`: The OpenAI language model to use for code review (defaults to `gpt-4o-mini`).
* `prompt`: A custom prompt for the analysis (defaults to an empty string).
* `max-length`: The maximum length of the diff sent to OpenAI for review (defaults to 450,000 characters).
* `post-if-error`: Whether to post a comment if there was an error (defaults to `true`).
* `excluded-files`: A list of files or directories to exclude from the review.

## Limitations

Please note that the 450,000 character limit is an estimated window of how much code can be sent to OpenAI. If your code exceeds this limit, it will be truncated, and only the first 450,000 characters will be reviewed. 
To avoid this issue:
- Break down large code changes into smaller PRs.
- Consider reviewing code in chunks, although this feature is not currently supported.

## Troubleshooting

* Check the GitHub Actions logs for error messages.
* Verify that your OpenAI API key is valid and properly configured.
* If you encounter any issues, please create an issue or pull request in the repository.

## Contributing

Contributions to this action are welcome! Please create an issue or pull request in the repository.

## License

This action is licensed under the Apache 2.0 License. See the LICENSE file for details.

## Changelog

See the CHANGELOG file for a record of changes, updates, and fixes.

## Author and Maintenance

* Author: [Chad Gauthier](https://github.com/chadgauth)
* Maintenance Status: Actively maintained by Chad Gauthier. Contributions and pull requests are welcome!