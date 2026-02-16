import time
import random
from pathlib import Path
from textual.screen import Screen
from textual.widgets import Static
from textual.events import Key


# Characters-per-keypress range for hackertyper effect
CHARS_PER_KEY_MIN = 3
CHARS_PER_KEY_MAX = 6

# How many blank lines above/below the cursor to center the typing area
CONTEXT_LINES_ABOVE = 25
CONTEXT_LINES_BELOW = 25


def _build_spreadsheet_lines():
    """Build a large spreadsheet as a list of lines for scrollable display."""
    lines = []
    lines.append("  Acme Corp — FY2025 Consolidated Financial Report (USD)")
    lines.append("  Generated: 2025-12-15 14:32:07  |  Confidential  |  Do Not Distribute")
    lines.append("")

    # --- Income Statement ---
    lines.append("  ╔══════════════════════════════════════════════════════════════════════════════════════════╗")
    lines.append("  ║  INCOME STATEMENT                                                                      ║")
    lines.append("  ╠══════════════════════════════════════════════════════════════════════════════════════════╣")
    hdr = "  ║ {:<24}│{:>14}│{:>14}│{:>14}│{:>14}│{:>14} ║"
    sep = "  ║─────────────────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────║"
    row = "  ║ {:<24}│{:>14}│{:>14}│{:>14}│{:>14}│{:>14} ║"

    lines.append(hdr.format("", "Q1 2025", "Q2 2025", "Q3 2025", "Q4 2025", "FY 2025"))
    lines.append(sep)

    income_data = [
        ("Product Revenue",      " 9,337,500",  " 9,840,000",  "11,167,500",  "11,505,000",  "41,850,000"),
        ("Service Revenue",      " 3,112,500",  " 3,280,000",  " 3,722,500",  " 3,835,000",  "13,950,000"),
        ("Total Revenue",        "12,450,000",  "13,120,000",  "14,890,000",  "15,340,000",  "55,800,000"),
        ("",                     "",            "",            "",            "",            ""),
        ("Cost of Goods Sold",   "(4,980,000)", "(5,248,000)", "(5,956,000)", "(6,136,000)", "(22,320,000)"),
        ("Gross Profit",         " 7,470,000",  " 7,872,000",  " 8,934,000",  " 9,204,000",  "33,480,000"),
        ("Gross Margin %",       "      60.0%", "      60.0%", "      60.0%", "      60.0%", "      60.0%"),
        ("",                     "",            "",            "",            "",            ""),
        ("R&D Expense",          "(2,490,000)", "(2,624,000)", "(2,978,000)", "(3,068,000)", "(11,160,000)"),
        ("Sales & Marketing",    "(1,868,000)", "(1,968,000)", "(2,234,000)", "(2,301,000)", "(8,370,000)"),
        ("General & Admin",      "  (623,000)", "  (656,000)", "  (745,000)", "  (767,000)", "(2,790,000)"),
        ("Total OpEx",           "(4,980,000)", "(5,248,000)", "(5,956,000)", "(6,136,000)", "(22,320,000)"),
        ("",                     "",            "",            "",            "",            ""),
        ("EBITDA",               " 2,490,000",  " 2,624,000",  " 2,978,000",  " 3,068,000",  "11,160,000"),
        ("EBITDA Margin %",      "      20.0%", "      20.0%", "      20.0%", "      20.0%", "      20.0%"),
        ("Depreciation & Amort", "  (498,000)", "  (525,000)", "  (596,000)", "  (614,000)", "(2,232,000)"),
        ("EBIT",                 " 1,992,000",  " 2,099,000",  " 2,382,000",  " 2,454,000",  " 8,928,000"),
        ("Interest Expense",     "  (187,000)", "  (197,000)", "  (223,000)", "  (230,000)", "  (837,000)"),
        ("Pre-Tax Income",       " 1,805,000",  " 1,902,000",  " 2,159,000",  " 2,224,000",  " 8,091,000"),
        ("Income Tax (25%)",     "  (451,000)", "  (476,000)", "  (540,000)", "  (556,000)", "(2,023,000)"),
        ("Net Income",           " 1,354,000",  " 1,427,000",  " 1,619,000",  " 1,668,000",  " 6,068,000"),
        ("Net Margin %",         "      10.9%", "      10.9%", "      10.9%", "      10.9%", "      10.9%"),
    ]
    for r in income_data:
        if not r[0]:
            lines.append(sep)
        else:
            lines.append(row.format(*r))
    lines.append("  ╚══════════════════════════════════════════════════════════════════════════════════════════╝")
    lines.append("")
    lines.append("")

    # --- Balance Sheet ---
    lines.append("  ╔══════════════════════════════════════════════════════════════════════════════════════════╗")
    lines.append("  ║  BALANCE SHEET (as of Dec 31, 2025)                                                    ║")
    lines.append("  ╠══════════════════════════════════════════════════════════════════════════════════════════╣")

    bs_hdr = "  ║ {:<40}│{:>14}│{:>14}│{:>14} ║"
    bs_sep = "  ║─────────────────────────────────────────┼──────────────┼──────────────┼──────────────║"
    bs_row = "  ║ {:<40}│{:>14}│{:>14}│{:>14} ║"

    lines.append(bs_hdr.format("", "2025", "2024", "Change %"))
    lines.append(bs_sep)

    balance_data = [
        ("ASSETS", "", "", ""),
        ("  Cash & Equivalents",              "18,240,000",  "14,500,000",  "   +25.8%"),
        ("  Short-Term Investments",          " 5,600,000",  " 4,200,000",  "   +33.3%"),
        ("  Accounts Receivable",             " 8,370,000",  " 7,100,000",  "   +17.9%"),
        ("  Inventory",                       " 3,348,000",  " 2,900,000",  "   +15.4%"),
        ("  Prepaid Expenses",                "   837,000",  "   720,000",  "   +16.3%"),
        ("Total Current Assets",              "36,395,000",  "29,420,000",  "   +23.7%"),
        ("",                                  "",            "",            ""),
        ("  Property, Plant & Equipment",     "11,160,000",  " 9,800,000",  "   +13.9%"),
        ("  Accumulated Depreciation",        "(4,464,000)", "(3,920,000)", "   +13.9%"),
        ("  Net PP&E",                        " 6,696,000",  " 5,880,000",  "   +13.9%"),
        ("  Goodwill",                        " 8,928,000",  " 8,928,000",  "    +0.0%"),
        ("  Intangible Assets",               " 3,348,000",  " 3,800,000",  "   -11.9%"),
        ("  Other Long-Term Assets",          " 1,116,000",  "   950,000",  "   +17.5%"),
        ("Total Non-Current Assets",          "20,088,000",  "19,558,000",  "    +2.7%"),
        ("",                                  "",            "",            ""),
        ("TOTAL ASSETS",                      "56,483,000",  "48,978,000",  "   +15.3%"),
        ("",                                  "",            "",            ""),
        ("LIABILITIES",                       "",            "",            ""),
        ("  Accounts Payable",                " 3,906,000",  " 3,400,000",  "   +14.9%"),
        ("  Accrued Expenses",                " 2,790,000",  " 2,350,000",  "   +18.7%"),
        ("  Short-Term Debt",                 " 1,674,000",  " 1,500,000",  "   +11.6%"),
        ("  Deferred Revenue",                " 4,464,000",  " 3,800,000",  "   +17.5%"),
        ("Total Current Liabilities",         "12,834,000",  "11,050,000",  "   +16.1%"),
        ("",                                  "",            "",            ""),
        ("  Long-Term Debt",                  " 8,370,000",  " 9,200,000",  "    -9.0%"),
        ("  Deferred Tax Liabilities",        " 1,674,000",  " 1,450,000",  "   +15.4%"),
        ("  Other Long-Term Liabilities",     "   558,000",  "   480,000",  "   +16.3%"),
        ("Total Non-Current Liabilities",     "10,602,000",  "11,130,000",  "    -4.7%"),
        ("",                                  "",            "",            ""),
        ("TOTAL LIABILITIES",                 "23,436,000",  "22,180,000",  "    +5.7%"),
        ("",                                  "",            "",            ""),
        ("EQUITY",                            "",            "",            ""),
        ("  Common Stock",                    " 1,116,000",  " 1,116,000",  "    +0.0%"),
        ("  Retained Earnings",               "31,931,000",  "25,682,000",  "   +24.3%"),
        ("Total Equity",                      "33,047,000",  "26,798,000",  "   +23.3%"),
        ("",                                  "",            "",            ""),
        ("TOTAL LIAB. + EQUITY",              "56,483,000",  "48,978,000",  "   +15.3%"),
    ]
    for r in balance_data:
        if not r[0]:
            lines.append(bs_sep)
        elif r[1] == "":
            # Section header
            lines.append(bs_row.format(r[0], "", "", ""))
        else:
            lines.append(bs_row.format(*r))
    lines.append("  ╚══════════════════════════════════════════════════════════════════════════════════════════╝")
    lines.append("")
    lines.append("")

    # --- Cash Flow Statement ---
    lines.append("  ╔══════════════════════════════════════════════════════════════════════════════════════════╗")
    lines.append("  ║  CASH FLOW STATEMENT (FY 2025)                                                         ║")
    lines.append("  ╠══════════════════════════════════════════════════════════════════════════════════════════╣")

    cf_row = "  ║ {:<54}│{:>14}│{:>14} ║"
    cf_sep = "  ║───────────────────────────────────────────────────────┼──────────────┼──────────────║"

    lines.append(cf_row.format("", "FY 2025", "FY 2024"))
    lines.append(cf_sep)

    cashflow_data = [
        ("OPERATING ACTIVITIES",                         "",            ""),
        ("  Net Income",                                 " 6,068,000",  " 5,120,000"),
        ("  Depreciation & Amortization",                " 2,232,000",  " 1,960,000"),
        ("  Stock-Based Compensation",                   " 1,674,000",  " 1,400,000"),
        ("  Changes in Working Capital",                 "  (558,000)", "  (320,000)"),
        ("Net Cash from Operations",                     " 9,416,000",  " 8,160,000"),
        ("",                                             "",            ""),
        ("INVESTING ACTIVITIES",                         "",            ""),
        ("  Capital Expenditures",                       "(2,790,000)", "(2,100,000)"),
        ("  Acquisitions",                               "         0",  "(4,500,000)"),
        ("  Purchases of Investments",                   "(1,400,000)", "(1,200,000)"),
        ("Net Cash from Investing",                      "(4,190,000)", "(7,800,000)"),
        ("",                                             "",            ""),
        ("FINANCING ACTIVITIES",                         "",            ""),
        ("  Debt Repayment",                             "  (830,000)", "  (600,000)"),
        ("  Share Repurchases",                          "  (656,000)", "  (500,000)"),
        ("Net Cash from Financing",                      "(1,486,000)", "(1,100,000)"),
        ("",                                             "",            ""),
        ("Net Change in Cash",                           " 3,740,000",  "  (740,000)"),
        ("Cash, Beginning of Period",                    "14,500,000",  "15,240,000"),
        ("Cash, End of Period",                          "18,240,000",  "14,500,000"),
    ]
    for r in cashflow_data:
        if not r[0]:
            lines.append(cf_sep)
        elif r[1] == "":
            lines.append(cf_row.format(r[0], "", ""))
        else:
            lines.append(cf_row.format(*r))
    lines.append("  ╚══════════════════════════════════════════════════════════════════════════════════════════╝")
    lines.append("")
    lines.append("")

    # --- Key Metrics ---
    lines.append("  ╔══════════════════════════════════════════════════════════════════════════════════════════╗")
    lines.append("  ║  KEY METRICS & KPIs                                                                    ║")
    lines.append("  ╠══════════════════════════════════════════════════════════════════════════════════════════╣")

    kpi_row = "  ║ {:<40}│{:>14}│{:>14}│{:>14} ║"
    kpi_sep = "  ║─────────────────────────────────────────┼──────────────┼──────────────┼──────────────║"

    lines.append(kpi_row.format("Metric", "2025", "2024", "YoY Change"))
    lines.append(kpi_sep)

    kpi_data = [
        ("Headcount (EoP)",                   "         361", "         298", "   +21.1%"),
        ("Revenue per Employee",              "     154,571", "     147,651", "    +4.7%"),
        ("Customer Count",                    "       2,847", "       2,340", "   +21.7%"),
        ("Annual Recurring Revenue (ARR)",    "52,200,000",   "43,800,000",  "   +19.2%"),
        ("Net Revenue Retention (NRR)",       "       118%",  "       115%",  "  +3.0 pp"),
        ("Customer Acquisition Cost (CAC)",   "      12,400", "      13,200", "    -6.1%"),
        ("LTV:CAC Ratio",                     "        4.2x", "        3.8x", "   +10.5%"),
        ("Monthly Active Users (MAU)",        "     284,700", "     234,000", "   +21.7%"),
        ("Churn Rate (Annual)",               "        8.2%", "        9.1%", "  -0.9 pp"),
        ("NPS Score",                         "          72", "          68", "    +5.9%"),
        ("Avg Contract Value (ACV)",          "      18,300", "      18,700", "    -2.1%"),
        ("Days Sales Outstanding (DSO)",      "          54", "          52", "    +3.8%"),
        ("Quick Ratio",                       "        2.6x", "        2.3x", "   +13.0%"),
        ("Debt-to-Equity",                    "       0.30x", "       0.40x", "   -25.0%"),
        ("Return on Equity (ROE)",            "      18.4%",  "      19.1%",  "  -0.7 pp"),
        ("Return on Assets (ROA)",            "      10.7%",  "      10.5%",  "  +0.2 pp"),
        ("Free Cash Flow",                    " 6,626,000",   " 6,060,000",  "    +9.3%"),
        ("FCF Margin",                        "      11.9%",  "      13.0%",  "  -1.1 pp"),
    ]
    for r in kpi_data:
        lines.append(kpi_row.format(*r))
    lines.append("  ╚══════════════════════════════════════════════════════════════════════════════════════════╝")
    lines.append("")

    # --- Regional Breakdown ---
    lines.append("  ╔══════════════════════════════════════════════════════════════════════════════════════════╗")
    lines.append("  ║  REVENUE BY REGION                                                                     ║")
    lines.append("  ╠══════════════════════════════════════════════════════════════════════════════════════════╣")

    reg_row = "  ║ {:<24}│{:>14}│{:>14}│{:>14}│{:>14}│{:>14} ║"
    reg_sep = "  ║─────────────────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────║"

    lines.append(reg_row.format("Region", "Q1 2025", "Q2 2025", "Q3 2025", "Q4 2025", "FY 2025"))
    lines.append(reg_sep)

    region_data = [
        ("North America",     " 6,225,000",  " 6,560,000",  " 7,445,000",  " 7,670,000",  "27,900,000"),
        ("EMEA",              " 3,735,000",  " 3,936,000",  " 4,467,000",  " 4,602,000",  "16,740,000"),
        ("APAC",              " 1,868,000",  " 1,968,000",  " 2,234,000",  " 2,301,000",  " 8,370,000"),
        ("LATAM",             "   622,000",  "   656,000",  "   744,000",  "   767,000",  " 2,790,000"),
        ("",                  "",            "",            "",            "",            ""),
        ("Total",             "12,450,000",  "13,120,000",  "14,890,000",  "15,340,000",  "55,800,000"),
    ]
    for r in region_data:
        if not r[0]:
            lines.append(reg_sep)
        else:
            lines.append(reg_row.format(*r))
    lines.append("  ╚══════════════════════════════════════════════════════════════════════════════════════════╝")
    lines.append("")

    # --- Product Breakdown ---
    lines.append("  ╔══════════════════════════════════════════════════════════════════════════════════════════╗")
    lines.append("  ║  REVENUE BY PRODUCT LINE                                                               ║")
    lines.append("  ╠══════════════════════════════════════════════════════════════════════════════════════════╣")
    lines.append(reg_row.format("Product", "Q1 2025", "Q2 2025", "Q3 2025", "Q4 2025", "FY 2025"))
    lines.append(reg_sep)

    product_data = [
        ("Platform Core",     " 5,602,500",  " 5,904,000",  " 6,700,500",  " 6,903,000",  "25,110,000"),
        ("Analytics Suite",   " 3,112,500",  " 3,280,000",  " 3,722,500",  " 3,835,000",  "13,950,000"),
        ("Enterprise Add-ons"," 2,490,000",  " 2,624,000",  " 2,978,000",  " 3,068,000",  "11,160,000"),
        ("Professional Svcs", " 1,245,000",  " 1,312,000",  " 1,489,000",  " 1,534,000",  " 5,580,000"),
        ("",                  "",            "",            "",            "",            ""),
        ("Total",             "12,450,000",  "13,120,000",  "14,890,000",  "15,340,000",  "55,800,000"),
    ]
    for r in product_data:
        if not r[0]:
            lines.append(reg_sep)
        else:
            lines.append(reg_row.format(*r))
    lines.append("  ╚══════════════════════════════════════════════════════════════════════════════════════════╝")
    lines.append("")
    lines.append("  Prepared by: Finance Dept  |  Report ID: FIN-2025-Q4-CONS  |  Confidential")
    lines.append("  Approved by: J. Richardson, CFO  |  Review Date: 2025-12-14")
    lines.append("")

    return lines


def _load_source_code():
    """Load all .py files from the car/ directory for hackertyper content."""
    car_dir = Path(__file__).parent.parent
    buffer_parts = []
    py_files = sorted(car_dir.rglob("*.py"))
    for py_file in py_files:
        try:
            rel_path = py_file.relative_to(car_dir.parent)
            content = py_file.read_text(encoding="utf-8", errors="replace")
            buffer_parts.append(f"# --- {rel_path} ---\n{content}\n\n")
        except Exception:
            continue
    return "".join(buffer_parts)


class BossKeyScreen(Screen):
    """A screen that disguises the game as work — hackertyper or spreadsheet mode."""

    _MOUNT_COOLDOWN = 0.25

    def __init__(self) -> None:
        super().__init__()
        self._source_buffer = _load_source_code()
        self._spreadsheet_lines = _build_spreadsheet_lines()
        self._cursor = 0
        self._mode = "hacker"  # "hacker" or "spreadsheet"
        self._mount_time = 0.0
        self._visible_text = ""
        self._scroll_offset = 0  # for spreadsheet scrolling

    def compose(self):
        yield Static(id="boss-key-display")
        yield Static(id="boss-key-statusbar")

    def on_mount(self) -> None:
        self._mount_time = time.time()
        # Start with a few lines already visible so it looks mid-session
        initial_chars = random.randint(800, 2000)
        self._cursor = min(initial_chars, len(self._source_buffer))
        self._visible_text = self._source_buffer[:self._cursor]
        self._update_display()

    def _get_terminal_height(self):
        """Get the usable display height (minus statusbar)."""
        try:
            return self.app.size.height - 2  # 1 for statusbar, 1 for margin
        except Exception:
            return 40

    def _update_display(self) -> None:
        """Update the display widget based on current mode."""
        display = self.query_one("#boss-key-display", Static)
        statusbar = self.query_one("#boss-key-statusbar", Static)

        if self._mode == "hacker":
            self._render_hacker(display, statusbar)
        else:
            self._render_spreadsheet(display, statusbar)

    def _render_hacker(self, display, statusbar):
        """Render hackertyper mode with cursor in the middle of the screen."""
        all_lines = self._visible_text.split("\n")
        total_visible = self._get_terminal_height()

        # Put the cursor line in the middle of the screen
        # Lines above cursor = already typed, lines below = empty
        cursor_line_idx = len(all_lines) - 1
        lines_above = min(CONTEXT_LINES_ABOVE, cursor_line_idx)
        start = max(0, cursor_line_idx - lines_above)
        code_lines = all_lines[start:cursor_line_idx + 1]

        # Pad below the cursor with blank lines to center the typing position
        lines_below = total_visible - len(code_lines)
        if lines_below > 0:
            code_lines.extend([""] * lines_below)

        # Pad above if we don't have enough lines yet, to push code to middle
        if cursor_line_idx < CONTEXT_LINES_ABOVE:
            pad_above = CONTEXT_LINES_ABOVE - cursor_line_idx
            code_lines = [""] * pad_above + code_lines

        display.update("\n".join(code_lines))

        # Build vim-like status bar
        current_line = len(all_lines)
        total_lines = self._source_buffer.count("\n") + 1
        current_file = "car/app.py"
        for line in reversed(all_lines[-50:]):
            if line.startswith("# --- ") and line.endswith(" ---"):
                current_file = line[6:-4]
                break
        pct = int((self._cursor / max(len(self._source_buffer), 1)) * 100)
        statusbar.update(
            f" -- INSERT --    {current_file}    "
            f"ln {current_line}, col 1    {pct}%"
        )

        # Apply hacker styling
        display.styles.background = "black"
        display.styles.color = "#00ff00"
        statusbar.styles.background = "#005f00"
        statusbar.styles.color = "#00ff00"

    def _render_spreadsheet(self, display, statusbar):
        """Render spreadsheet mode with arrow-key scrolling."""
        total_visible = self._get_terminal_height()
        total_lines = len(self._spreadsheet_lines)

        # Clamp scroll offset
        max_offset = max(0, total_lines - total_visible)
        self._scroll_offset = max(0, min(self._scroll_offset, max_offset))

        visible = self._spreadsheet_lines[self._scroll_offset:self._scroll_offset + total_visible]
        display.update("\n".join(visible))

        # Statusbar with scroll position
        end_row = min(self._scroll_offset + total_visible, total_lines)
        statusbar.update(
            f" Sheet1  |  Ready  |  Rows {self._scroll_offset + 1}-{end_row} of {total_lines}"
            f"  |  ↑↓ Scroll  |  Tab: Switch Mode  |  Esc: Exit"
        )

        # Apply spreadsheet styling
        display.styles.background = "#1a1a2e"
        display.styles.color = "#e0e0e0"
        statusbar.styles.background = "#16213e"
        statusbar.styles.color = "#a0a0a0"

    def on_key(self, event: Key) -> None:
        """Handle all key events."""
        event.prevent_default()
        event.stop()

        # Cooldown check to prevent instant close
        if time.time() - self._mount_time < self._MOUNT_COOLDOWN:
            return

        if event.key in ("escape", "f12"):
            self.app.pop_screen()
            return

        if event.key == "tab":
            self._mode = "spreadsheet" if self._mode == "hacker" else "hacker"
            self._update_display()
            return

        # Spreadsheet mode: arrow keys scroll, everything else ignored
        if self._mode == "spreadsheet":
            if event.key == "up":
                self._scroll_offset = max(0, self._scroll_offset - 1)
                self._update_display()
            elif event.key == "down":
                self._scroll_offset += 1
                self._update_display()
            elif event.key == "pageup":
                self._scroll_offset = max(0, self._scroll_offset - self._get_terminal_height())
                self._update_display()
            elif event.key == "pagedown":
                self._scroll_offset += self._get_terminal_height()
                self._update_display()
            elif event.key == "home":
                self._scroll_offset = 0
                self._update_display()
            elif event.key == "end":
                self._scroll_offset = len(self._spreadsheet_lines)
                self._update_display()
            return

        # In hacker mode, any other key advances the cursor
        advance = random.randint(CHARS_PER_KEY_MIN, CHARS_PER_KEY_MAX)
        new_cursor = min(self._cursor + advance, len(self._source_buffer))

        # If we've reached the end, wrap around
        if new_cursor >= len(self._source_buffer):
            self._cursor = 0
            self._visible_text = ""
            new_cursor = advance

        self._visible_text += self._source_buffer[self._cursor:new_cursor]
        self._cursor = new_cursor
        self._update_display()
