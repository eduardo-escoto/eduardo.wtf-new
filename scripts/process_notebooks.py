# pull notebooks from github repo to /public/notebooks

# run nbconvert over all of them with custom template that pulls the metadata from notebook
# skip all notebooks with missing key metadata


# move compiled markdown to the /data/notebooks directory
# move compiled images to public/images

# make this a pre-commit script so that the notebook directory is up to date before commiting
# make a github action that re-commits to this repo whenever i commit to that notebook monorepo

import os
from datetime import datetime
from pathlib import Path

import nbformat
import yaml
from jinja2 import DictLoader
from nbconvert import MarkdownExporter
from slugify import slugify

# Note: preserve file structure as much as possible
# Note: I think the best way for this to work is with git hooks that
# update the repo with the latest updates from blog repo and notebook repo
template_creator = (
    lambda path_prefix: f"""
{{% extends 'markdown/index.md.j2' %}}
{{% block data_png %}}
    {{% if "filenames" in output.metadata %}}
![png]({path_prefix}{{{{ output.metadata.filenames['image/png'] | path2url }}}})
    {{% else %}}
![png](data:image/png;base64,{{{{ output.data['image/png'] }}}})
    {{% endif %}}
{{% endblock data_png %}}
"""
)


nb_folder_path = Path("./public/notebooks")

output_markdown_path = Path("./data/blog")
output_images_path = Path("./public/images")


default_fm = lambda title: {
    "title": title,
    "date": datetime.today().strftime("%Y-%m-%d"),
}


if __name__ == "__main__":
    for notebook_path in nb_folder_path.glob("*.ipynb"):
        output_folder = slugify(notebook_path.stem)

        out_j2 = template_creator(str(Path("/images") / output_folder) + "/")
        dl = DictLoader({"img": out_j2})

        md_exporter = MarkdownExporter(extra_loaders=[dl], template_file="img")

        with open(notebook_path, "r") as f:
            nb = nbformat.reads(f.read(), as_version=4)
            (body, resources) = md_exporter.from_notebook_node(nb)
            fm = (
                "---\r\n"
                + yaml.dump(
                    {
                        **default_fm(notebook_path.stem),
                        **dict(nb["metadata"]["frontmatter"]),
                    }
                    if "frontmatter" in dict(nb["metadata"]).keys()
                    else default_fm(notebook_path.stem)
                )
                + "---"
            )
            body = fm + "\r\n" + body

            for output_file, output_bytes in resources["outputs"].items():
                filename = str(output_images_path / output_folder) + f"/{output_file}"
                os.makedirs(os.path.dirname(filename), exist_ok=True)
                with open(filename, "wb") as output_file:
                    output_file.write(output_bytes)

            with open(
                str(output_markdown_path / output_folder) + ".mdx", "w"
            ) as output_file:
                output_file.write(body)
