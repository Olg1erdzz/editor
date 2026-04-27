// import { Language } from '@tiptap-pro/extension-ai'
import { Editor } from "@tiptap/vue-3";

export const useTextmenuCommands = (editor: Editor) => {
  const onBold = () => {
    editor.chain().focus().toggleBold().run();
  };

  const onItalic = () => {
    editor.chain().focus().toggleItalic().run();
  };
  const onStrike = () => {
    editor.chain().focus().toggleStrike().run();
  };
  const onUnderline = () => {
    editor.chain().focus().toggleUnderline().run();
  };
  const onCode = () => {
    editor.chain().focus().toggleCode().run();
  };
  const onCodeBlock = () => {
    editor.chain().focus().toggleCodeBlock().run();
  };

  const onSubscript = () => {
    editor.chain().focus().toggleSubscript().run();
  };
  const onSuperscript = () => {
    editor.chain().focus().toggleSuperscript().run();
  };
  const onAlignLeft = () => {
    editor.chain().focus().setTextAlign("left").run();
  };
  const onAlignCenter = () => {
    editor.chain().focus().setTextAlign("center").run();
  };
  const onAlignRight = () => {
    editor.chain().focus().setTextAlign("right").run();
  };
  const onAlignJustify = () => {
    editor.chain().focus().setTextAlign("justify").run();
  };

  const onChangeColor = () => {
    (color: string) => editor.chain().setColor(color).run();
  };
  const onClearColor = () => {
    editor.chain().focus().unsetColor().run();
  };

  const onChangeHighlight = () => {
    (color: string) => editor.chain().setHighlight({ color }).run();
  };
  const onClearHighlight = () => {
    editor.chain().focus().unsetHighlight().run();
  };

  // const onSimplify = () => {editor.chain().focus().aiSimplify().run(); }
  // const onEmojify = () => {editor.chain().focus().aiEmojify().run(); }
  // const onCompleteSentence = () => {editor.chain().focus().aiComplete().run(); }
  // const onFixSpelling = () => {editor.chain().focus().aiFixSpellingAndGrammar().run(); }
  // const onMakeLonger = () => {editor.chain().focus().aiExtend().run(); }
  // const onMakeShorter = () => {editor.chain().focus().aiShorten().run(); }
  // const onTldr = () => {editor.chain().focus().aiTldr().run(); }
  // const onTone = () => {(tone: string) => editor.chain().focus().aiAdjustTone(tone).run(); }
  // const onTranslate = () => {(language: Language) => editor.chain().focus().aiTranslate(language).run(); }
  const onLink = () => {
    (url: string, inNewTab?: boolean) =>
      editor
        .chain()
        .focus()
        .setLink({ href: url, target: inNewTab ? "_blank" : "" })
        .run();
  };

  const onSetFont = () => {
    (font: string) => {
      if (!font || font.length === 0) {
        return editor.chain().focus().unsetFontFamily().run();
      }
      return editor.chain().focus().setFontFamily(font).run();
    };
  };

  const onSetFontSize = () => {
    (fontSize: string) => {
      if (!fontSize || fontSize.length === 0) {
        return editor.chain().focus().unsetFontSize().run();
      }
      return editor.chain().focus().setFontSize(fontSize).run();
    };
  };

  return {
    onBold,
    onItalic,
    onStrike,
    onUnderline,
    onCode,
    onCodeBlock,
    onSubscript,
    onSuperscript,
    onAlignLeft,
    onAlignCenter,
    onAlignRight,
    onAlignJustify,
    onChangeColor,
    onClearColor,
    onChangeHighlight,
    onClearHighlight,
    onSetFont,
    onSetFontSize,
    onSimplify,
    onEmojify,
    onCompleteSentence,
    onFixSpelling,
    onMakeLonger,
    onMakeShorter,
    onTldr,
    onTone,
    onTranslate,
    onLink
  };
};
