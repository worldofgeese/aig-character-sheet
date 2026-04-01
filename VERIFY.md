# Post-Fix Verification Plan

## Gate 1: Structural
- [ ] Tests pass: `pytest tests/test_calculations.py -v`
- [ ] HTML is valid single file
- [ ] All JSON data embedded correctly
- [ ] Diff review: changes scoped to the 5 fixes only

## Gate 1.5: Manual Exercise (Playwright)
- [ ] Open aig-character-sheet.html in browser
- [ ] Walk through all 12 wizard steps end-to-end
- [ ] Step 2: Test both point-buy and dice roller
- [ ] Step 4: Select Sartarite/Heortling → verify auto-fill
- [ ] Step 5: Verify cultural skills populated, distribute 100 points, verify budget enforcement
- [ ] Step 8: Select Warrior → verify career skills auto-populate
- [ ] Step 9: Pick 3 professional skills, distribute 100 career points
- [ ] Step 10: Verify accumulated skills shown, distribute bonus points, verify age cap
- [ ] Step 11: Test weapon autocomplete — type "Broad", verify filtered results appear
- [ ] Step 12: Enter play mode, verify all derived values
- [ ] Play mode: Test difficulty modifier dropdown
- [ ] Play mode: Test special effects panel expand/collapse
- [ ] Mobile: Test at 375px width — verify Remove buttons visible
- [ ] Print: Test A4 portrait print button
- [ ] Screenshot each step for evidence

## Gate 2: Judge Agent
- [ ] Fresh-context review of diff against fix brief
- [ ] Mechanical verification of career skills data (24 careers × 7+7 skills)
- [ ] Formula preservation check (no regressions in calculations)

## Playwright Command
```bash
devbox run playwright-cli -- screenshot \
  --url "file:///tmp/aig-character-sheet/aig-character-sheet.html" \
  --viewport "375x812" \
  --output /tmp/aig-mobile-test.png

devbox run playwright-cli -- screenshot \
  --url "file:///tmp/aig-character-sheet/aig-character-sheet.html" \
  --viewport "1440x900" \
  --output /tmp/aig-desktop-test.png
```
