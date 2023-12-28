# pull notebooks from github repo to /public/notebooks

# run nbconvert over all of them with custom template that pulls the metadata from notebook
    # skip all notebooks with missing key metadata

# move compiled markdown to the /data/notebooks directory
# move compiled images to public/images

# make this a pre-commit script so that the notebook directory is up to date before commiting
    # make a github action that re-commits to this repo whenever i commit to that notebook monorepo

# Note: preserve file structure as much as possible
# Note: I think the best way for this to work is with git hooks that 
# update the repo with the latest updates from blog repo and notebook repo