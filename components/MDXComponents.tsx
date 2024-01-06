import TOCInline from 'pliny/ui/TOCInline'
import Pre from 'pliny/ui/Pre'
import BlogNewsletterForm from 'pliny/ui/BlogNewsletterForm'
import type { MDXComponents } from 'mdx/types'
import Image from './Image'
import CustomLink from './Link'
import TableWrapper from './TableWrapper'
import { ImageProps } from 'next/image'

export const components: MDXComponents = {
  Image: ({ ...rest }: ImageProps) => (
    <div className="flex items-center justify-center">
      <Image className="bg-white" {...rest} />{' '}
    </div>
  ),
  TOCInline,
  a: CustomLink,
  pre: Pre,
  table: TableWrapper,
  BlogNewsletterForm,
}
