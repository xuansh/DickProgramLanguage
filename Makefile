# run:
	python3 main.py $(DIR)

# 颜色定义
# RED    := \033[0;31m
# GREEN  := \033[0;32m
# YELLOW := \033[0;33m
# BLUE   := \033[0;34m
# CYAN   := \033[0;36m
# RESET  := \033[0m

# DIR ?= .

# run:
# 	@echo "$(CYAN)╔════════════════════════════════════╗$(RESET)"
# 	@echo "$(CYAN)║  🚀  Starting Application       ║$(RESET)"
# 	@echo "$(CYAN)╚════════════════════════════════════╝$(RESET)"
# 	@echo "$(GREEN)► Directory:$(YELLOW) $(DIR)$(RESET)"
# 	@echo "$(GREEN)► Time:$(YELLOW) $$(date '+%Y-%m-%d %H:%M:%S')$(RESET)"
# 	@echo ""
# 	@python3 main.py $(DIR) || { \
# 		echo "$(RED)✗ Execution failed!$(RESET)"; \
# 		exit 1; \
# 	}
# 	@echo "$(GREEN)✓ Done!$(RESET)"
