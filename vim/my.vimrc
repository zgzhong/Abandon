" **********vundle环境配置*******
filetype off
set rtp+=~/.vim/bundle/Vundle.vim
" vundle 管理的插件列表必须位于 vundle#begin() 和 vundle#end()之间
call vundle#begin()
Plugin 'VundleVim/Vundle.vim'               " vundle插件
Plugin 'altercation/vim-colors-solarized'   " solarized 主题
Plugin 'tomasr/molokai'                     " molokai 主题
Plugin 'vim-scripts/phd'                    " phd 主题
Plugin 'Lokaltog/vim-powerline'
Plugin 'octol/vim-cpp-enhanced-highlight'   
Plugin 'nathanaelkane/vim-indent-guides'    " 对齐线插件 
Plugin 'derekwyatt/vim-fswitch'
Plugin 'kshenoy/vim-signature'
Plugin 'vim-scripts/BOOKMARKS--Mark-and-Highlight-Full-Lines'
Plugin 'majutsushi/tagbar'
Plugin 'vim-scripts/indexer.tar.gz'
Plugin 'vim-scripts/DfrankUtil'
Plugin 'vim-scripts/vimprj'
Plugin 'dyng/ctrlsf.vim'
Plugin 'terryma/vim-multiple-cursors'
Plugin 'scrooloose/nerdcommenter'
Plugin 'vim-scripts/DrawIt'
Plugin 'SirVer/ultisnips'
Plugin 'Valloric/YouCompleteMe'
Plugin 'derekwyatt/vim-protodef'
Plugin 'scrooloose/nerdtree'
Plugin 'fholgado/minibufexpl.vim'
Plugin 'gcmt/wildfire.vim'
Plugin 'sjl/gundo.vim'
Plugin 'Lokaltog/vim-easymotion'
call vundle#end()
filetype plugin indent on
" *******************************


" *************快捷键配置********
" 定义快捷键的前缀，即<Leader>
let mapleader=","
" 把jk快捷键映射到ESC
:imap kj <ESC>
" 在常规模式下把; 映射到:
:nmap ; :
" 定义快捷键到行首行尾
nmap LB 0
nmap LB $
" 定义快捷键关闭当前分割窗口
nmap <Leader>q :q<cr>
" 定义快捷键保存当前窗口的内容
nmap <Leader>w :w<cr>
" 定义快捷键保存所有窗口内容并退出vim
nmap <Leader>WQ :wa<cr>:q<cr>
" 跳转至右方的窗口
nnoremap <C-l> <C-W>l
" 跳转至左方的窗口
nnoremap <C-h> <C-W>h
" 跳转至上方的子窗口
nnoremap <C-k> <C-W>k
" 跳转至下方的子窗口
nnoremap <C-j> <C-W>j 
" 定义快捷键在结对符之间跳转
nmap <Leader><Space> %
" *******************************

" ************UI 配置************
" 配色方案
set background=dark
colorscheme molokai "solarized phd
" 开启行号
set number
" 开启语法高亮功能
 syntax enable
"开启语法高亮
syntax on
" 禁止代码拆行
set nowrap
" 十字架光标
set cursorline cursorcolumn
" 总是显示状态栏
set laststatus=2
" 设置状态栏主题风格
let g:Powerline_colorscheme='solarized256'
" ******************************

" ***********制表符配置*********
"将制表符变换为空格
set expandtab
" 编辑时制表符占用空格数
set tabstop=4
" 设置格式化时制表符占用空格数
set shiftwidth=4
" 让vim把连续数量的空格是视为一个tab
set softtabstop=4
" Makefile 不转换tab为空格
autocmd FileType make setlocal noexpandtab
" *****************************

" ******搜索,命令补全设置******
" 开启实时搜索功能
set incsearch
" 搜索时大小写不敏感
set ignorecase
" 关闭兼容模式
set nocompatible
" vim 自身命令行模式智能 补全
set wildmenu
" *****************************

" **缩进对其配置 ident guides**
" 随 vim 自启动
let g:indent_guides_enable_on_vim_startup=1
" 从第二层开始可视化显式缩进
let g:indent_guides_start_level=2
" 色块宽度
let g:indent_guides_guide_size=1
" 快捷键 i 开/关缩进可视化
:nmap <silent> <Leader>i <Plug>IndentGuidesToggle
" *****************************

" ******* 代码折叠配置 ********
" 基于缩进或语法进行代码折叠
set foldmethod=syntax
" 启动时关闭代码折叠
set nofoldenable
" *****************************

" *** 基于标签的表示符列表 ****
" 设置 tagbar 子窗口的位置出现在主编辑区的左边 
let tagbar_left=1 
" 设置显示／隐藏标签列表子窗口的快捷键。速记：tag list
nnoremap <silent> <Leader>tl :TagbarToggle<CR> 
" 设置标签子窗口的宽度 
let tagbar_width=16
" tagbar 子窗口中不显示冗余帮助信息 
let g:tagbar_compact=1
" 设置 ctags 对哪些代码标识符生成标签
let g:tagbar_type_cpp = {
    \ 'kinds' : [
         \ 'c:classes:0:1',
         \ 'd:macros:0:1',
         \ 'e:enumerators:0:0', 
         \ 'f:functions:0:1',
         \ 'g:enumeration:0:1',
         \ 'l:local:0:1',
         \ 'm:members:0:1',
         \ 'n:namespaces:0:1',
         \ 'p:functions_prototypes:0:1',
         \ 's:structs:0:1',
         \ 't:typedefs:0:1',
         \ 'u:unions:0:1',
         \ 'v:global:0:1',
         \ 'x:external:0:1'
     \ ],
     \ 'sro'        : '::',
     \ 'kind2scope' : {
         \ 'g' : 'enum',
         \ 'n' : 'namespace',
         \ 'c' : 'class',
         \ 's' : 'struct',
         \ 'u' : 'union'
     \ },
     \ 'scope2kind' : {
         \ 'enum'      : 'g',
         \ 'namespace' : 'n',
         \ 'class'     : 'c',
         \ 'struct'    : 's',
         \ 'union'     : 'u'
     \ }
\ }
" *****************************

" 忽略基于标签的声明定义跳转 

" ********* YCM 配置 *********
" 跳转到声明 jdl 表示jump decleration
nnoremap <leader>dl :YcmCompleter GoToDeclaration<CR>
" 跳转到定义 jdf 表示jump definition  只能是 #include 或已打开的文件 
nnoremap <leader>df :YcmCompleter GoToDefinition<CR>
" 补全功能在注释中同样有效
let g:ycm_complete_in_comments=1
" 允许 vim 加载 .ycm_extra_conf.py 文件，不再提示
let g:ycm_confirm_extra_conf=0
" 开启 YCM 标签补全引擎
let g:ycm_collect_identifiers_from_tags_files=1
" 引入 C++ 标准库tags
set tags+=/data/misc/software/misc./vim/stdcpp.tags
" YCM 集成 OmniCppComplete 补全引擎，设置其快捷键
inoremap <leader>, <C-x><C-o>
" 补全内容不以分割子窗口形式出现，只显示补全列表
set completeopt-=preview
" 从第二个键入字符就开始罗列匹配项
let g:ycm_min_num_of_chars_for_completion=2
" 禁止缓存匹配项，每次都重新生成匹配项
let g:ycm_cache_omnifunc=0
" 语法关键字补全
let g:ycm_seed_identifiers_with_syntax=1
" ****************************

" +----+---------+  
" |4.8 | 内容查找|
" +----+---------+   
" |4.9 | 内容替换|
" +----+---------+ 

" ******* Snippets 配置 ******
" 补全代码片段的文件夹
let g:UltiSnipsSnippetDirectories=["mysnippets"]
" UltiSnips 的 tab 键与 YCM 冲突，重新设定
let g:UltiSnipsExpandTrigger="<leader><tab>"
let g:UltiSnipsJumpForwardTrigger="<leader><tab>"
let g:UltiSnipsJumpBackwardTrigger="<leader><s-tab>"
" ****************************

" *********杂项配置***********
" *.cpp 和 *.h 间切换
nmap <silent> <Leader>sw :FSHere<cr>
" ****************************


" TODO: 5.3 只能补全
