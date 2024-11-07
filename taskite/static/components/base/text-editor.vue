<template>
    <div class="border border-gray-200 rounded-lg">
        <div class="flex flex-wrap gap-2 p-2 border-b border-gray-200 bg-gray-50 rounded-t-lg">
            <Space>
                <Tooltip title="Bold">
                    <Button :type="editor?.isActive('bold') ? 'primary' : 'default'"
                        @click="editor?.chain().focus().toggleBold().run()" class="px-3">
                        <template #icon>
                            <BoldOutlined />
                        </template>
                    </Button>
                </Tooltip>

                <Tooltip title="Italic">
                    <Button :type="editor?.isActive('italic') ? 'primary' : 'default'"
                        @click="editor?.chain().focus().toggleItalic().run()" class="px-3">
                        <template #icon>
                            <ItalicOutlined />
                        </template>
                    </Button>
                </Tooltip>

                <Tooltip title="Strikethrough">
                    <Button :type="editor?.isActive('strike') ? 'primary' : 'default'"
                        @click="editor?.chain().focus().toggleStrike().run()" class="px-3">
                        <template #icon>
                            <StrikethroughOutlined />
                        </template>
                    </Button>
                </Tooltip>
            </Space>

            <Divider type="vertical" class="h-8" />

            <Space>
                <Select class="w-32" :value="currentHeading" @change="setHeading" size="middle">
                    <SelectOption value="">Paragraph</SelectOption>
                    <SelectOption value="1">Heading 1</SelectOption>
                    <SelectOption value="2">Heading 2</SelectOption>
                    <SelectOption value="3">Heading 3</SelectOption>
                </Select>
            </Space>

            <Divider type="vertical" class="h-8" />

            <Space>
                <Tooltip title="Bullet List">
                    <Button :type="editor?.isActive('bulletList') ? 'primary' : 'default'"
                        @click="editor?.chain().focus().toggleBulletList().run()" class="px-3">
                        <template #icon>
                            <UnorderedListOutlined />
                        </template>
                    </Button>
                </Tooltip>

                <Tooltip title="Numbered List">
                    <Button :type="editor?.isActive('orderedList') ? 'primary' : 'default'"
                        @click="editor?.chain().focus().toggleOrderedList().run()" class="px-3">
                        <template #icon>
                            <OrderedListOutlined />
                        </template>
                    </Button>
                </Tooltip>
            </Space>

            <Divider type="vertical" class="h-8" />

            <Space>
                <Tooltip title="Code">
                    <Button :type="editor?.isActive('code') ? 'primary' : 'default'"
                        @click="editor?.chain().focus().toggleCode().run()" class="px-3">
                        <template #icon>
                            <CodeOutlined />
                        </template>
                    </Button>
                </Tooltip>

                <Tooltip title="Code Block">
                    <Button :type="editor?.isActive('codeBlock') ? 'primary' : 'default'"
                        @click="editor?.chain().focus().toggleCodeBlock().run()" class="px-3">
                        <template #icon>
                            <CodepenOutlined />
                        </template>
                    </Button>
                </Tooltip>
            </Space>

            <Divider type="vertical" class="h-8" />

            <Space>
                <Tooltip title="Quote">
                    <Button :type="editor?.isActive('blockquote') ? 'primary' : 'default'"
                        @click="editor?.chain().focus().toggleBlockquote().run()" class="px-3">
                        <template #icon>
                            <MessageOutlined />
                        </template>
                    </Button>
                </Tooltip>

                <Tooltip title="Horizontal Rule">
                    <Button @click="editor?.chain().focus().setHorizontalRule().run()" class="px-3">
                        <template #icon>
                            <MinusOutlined />
                        </template>
                    </Button>
                </Tooltip>
            </Space>
        </div>

        <editor-content :editor="editor" class="prose max-w-none" />
    </div>
</template>

<script setup>
import { ref, watch, onMounted, onBeforeUnmount, computed } from 'vue'
import StarterKit from '@tiptap/starter-kit'
import { Editor, EditorContent } from '@tiptap/vue-3'
import {
    BoldOutlined,
    ItalicOutlined,
    StrikethroughOutlined,
    UnorderedListOutlined,
    OrderedListOutlined,
    CodeOutlined,
    CodepenOutlined,
    MessageOutlined,
    MinusOutlined,
} from '@ant-design/icons-vue'
import { Button, Divider, Select, SelectOption, Space, Tooltip } from 'ant-design-vue';

const props = defineProps({
    modelValue: {
        type: String,
        default: '',
    },
})

const emit = defineEmits(['update:modelValue'])

const editor = ref(null)

const currentHeading = computed(() => {
    if (!editor.value) return ''
    if (editor.value.isActive('heading', { level: 1 })) return '1'
    if (editor.value.isActive('heading', { level: 2 })) return '2'
    if (editor.value.isActive('heading', { level: 3 })) return '3'
    return ''
})

const setHeading = (value) => {
    if (!value) {
        editor.value?.chain().focus().setParagraph().run()
    } else {
        editor.value?.chain().focus().toggleHeading({ level: parseInt(value) }).run()
    }
}

watch(
    () => props.modelValue,
    (value) => {
        if (!editor.value) return
        const isSame = editor.value.getHTML() === value
        if (isSame) return
        editor.value.commands.setContent(value, false)
    }
)

onMounted(() => {
    editor.value = new Editor({
        extensions: [
            StarterKit,
        ],
        content: props.modelValue,
        onUpdate: () => {
            emit('update:modelValue', editor.value.getHTML())
        },
    })
})

onBeforeUnmount(() => {
    editor.value?.destroy()
})
</script>

<style lang="scss">
.tiptap {
    @apply p-4;

    &:focus {
        @apply outline-none;
    }

    p {
        @apply my-4;
    }

    /* Heading styles */
    h1 {
        @apply text-3xl font-bold mt-8 mb-4;
    }

    h2 {
        @apply text-2xl font-bold mt-8 mb-4;
    }

    h3 {
        @apply text-xl font-bold mt-6 mb-4;
    }

    /* List styles */
    ul,
    ol {
        @apply pl-6 my-4;
    }

    li>p {
        @apply my-1;
    }

    /* Code styles */
    code {
        @apply bg-gray-100 text-gray-800 rounded px-1.5 py-0.5 text-sm;
    }

    pre {
        @apply bg-gray-900 text-white rounded-lg p-4 my-4 overflow-x-auto;

        code {
            @apply bg-transparent text-white p-0;
        }
    }

    /* Blockquote styles */
    blockquote {
        @apply border-l-4 border-gray-300 pl-4 my-4 italic;
    }

    /* Horizontal rule */
    hr {
        @apply border-t border-gray-200 my-8;
    }
}
</style>