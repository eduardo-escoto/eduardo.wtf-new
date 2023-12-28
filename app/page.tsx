import { sortPosts, allCoreContent } from 'pliny/utils/contentlayer'
import { allBlogs, allAuthors, Authors } from 'contentlayer/generated'
import { coreContent } from 'pliny/utils/contentlayer'
import Main from './Main'

export default async function Page() {
  const sortedPosts = sortPosts(allBlogs)
  const posts = allCoreContent(sortedPosts)

  const author = allAuthors.find((p) => p.slug === 'default') as Authors
  const authorContent = coreContent(author)

  return <Main posts={posts} author={author} authorContent={authorContent} />
}
