# Color shortcuts
RED=$fg[red]
YELLOW=$fg[yellow]
GREEN=$fg[green]
WHITE=$fg[white]
BLUE=$fg[blue]
CYAN=$fg[cyan]
MAGENTA=$fg[magenta]
RED_BOLD=$fg_bold[red]
YELLOW_BOLD=$fg_bold[yellow]
GREEN_BOLD=$fg_bold[green]
WHITE_BOLD=$fg_bold[white]
BLUE_BOLD=$fg_bold[blue]

# Format for git_prompt_status()
ZSH_THEME_GIT_PROMPT_UNMERGED=" %{$RED%}unmerged"
ZSH_THEME_GIT_PROMPT_DELETED=" %{$RED%}deleted"
ZSH_THEME_GIT_PROMPT_RENAMED=" %{$YELLOW%}renamed"
ZSH_THEME_GIT_PROMPT_MODIFIED=" %{$YELLOW%}modified"
ZSH_THEME_GIT_PROMPT_ADDED=" %{$GREEN%}added"
ZSH_THEME_GIT_PROMPT_UNTRACKED=" %{$WHITE%}untracked"

# Format for git_prompt_long_sha() and git_prompt_short_sha()
ZSH_THEME_GIT_PROMPT_SHA_BEFORE=" %{$BLUE_BOLD%}"
ZSH_THEME_GIT_PROMPT_SHA_AFTER="%{$reset_color%}"

# Format for git_prompt_info
ZSH_THEME_GIT_PROMPT_PREFIX=" %{$YELLOW%}git:%{$WHITE%}(%{$YELLOW%}"
ZSH_THEME_GIT_PROMPT_SUFFIX="%{$WHITE%})%{$reset_color%}"

# Format for git_prompt_status()
ZSH_THEME_GIT_PROMPT_UNMERGED="|%{$RED_BOLD%}unmerged%{$reset_color%}"
ZSH_THEME_GIT_PROMPT_DELETED="|%{$RED%}deleted%{$reset_color%}"
ZSH_THEME_GIT_PROMPT_RENAMED="|%{$YELLOW_BOLD%}renamed%{$reset_color%}"
ZSH_THEME_GIT_PROMPT_MODIFIED="|%{$YELLOW%}modified%{$reset_color%}"
ZSH_THEME_GIT_PROMPT_ADDED="|%{$GREEN%}added%{$reset_color%}"
ZSH_THEME_GIT_PROMPT_UNTRACKED="|%{$MAGENTA%}untracked%{$reset_color%}"

# PROMPT="[%*] %n:%c $(git_prompt_info)%(!.#.$) "
# %*: 显示时间
# %n: 用户名
# %c: 当前目录名
PROMPT='%{$CYAN%}%n%{$reset_color%}:%{$GREEN%}%c%{$reset_color%}$(git_prompt_info)$(git_prompt_short_sha)$(git_prompt_status) %(!.#.$) '
