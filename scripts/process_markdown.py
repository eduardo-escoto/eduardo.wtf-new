import os
from datetime import datetime
from pathlib import Path

import frontmatter
from slugify import slugify

input_base_path = Path("./public/blog-posts")
output_base_path = Path("./data/blog")


if __name__ == "__main__":
    for md_path in input_base_path.glob("*.md"):
        print(f"processing: {md_path.stem}")

        if md_path.stem != "README":
            output_path = output_base_path / Path(f"{slugify(md_path.stem)}.mdx")

            print(f"old path:{md_path}")
            print(f"new path:{output_path}")

            post = frontmatter.load(md_path)

            if "title" not in post.metadata.keys():
                post.metadata["title"] = output_path.stem

            if "date" not in post.metadata.keys():
                post.metadata["date"] = datetime.today().strftime("%Y-%m-%d")

            with open(output_path, "wb") as outfile:
                frontmatter.dump(post, outfile)
