# Bulk refactor all GUI modules to use dependency injection
# This script replaces self.gui.* references with dependency-specific calls

$files = @(
    'gui_achievements.py',
    'gui_quests.py', 
    'gui_inventory.py',
    'gui_save_load.py',
    'gui_bounty.py',
    'gui_blacksmith.py',
    'gui_shop.py',
    'gui_monster_encounter.py',
    'gui_tavern.py',
    'gui_town.py'
)

$replacements = @{
    'self\.gui\.root\.after' = 'self.timer.after'
    'self\.gui\.audio\.play_sound_effect' = 'self.audio.play_sound_effect'
    'self\.gui\.audio\.stop_music' = 'self.audio.stop_music'
    'self\.gui\.print_text' = 'self.text_display.print_text'
    'self\.gui\.clear_text' = 'self.text_display.clear_text'
    'self\.gui\.print_combat_damage' = 'self.text_display.print_combat_damage'
    'self\.gui\._print_colored_parts' = 'self.text_display._print_colored_parts'
    'self\.gui\.show_image' = 'self.image_display.show_image'
    'self\.gui\.show_images' = 'self.image_display.show_images'
    'self\.gui\._clear_foreground_images' = 'self.image_display._clear_foreground_images'
    'self\.gui\._add_canvas_image' = 'self.image_display._add_canvas_image'
    'self\.gui\._get_canvas_dimensions' = 'self.image_display._get_canvas_dimensions'
    'self\.gui\.lock_interface' = 'self.interface_control.lock_interface'
    'self\.gui\.unlock_interface' = 'self.interface_control.unlock_interface'
    'self\.gui\.set_buttons' = 'self.button_manager.set_buttons'
    'self\.gui\.show_buttons' = 'self.button_manager.show_buttons'
    'self\.gui\.game_state' = 'self.game_state'
    'self\.gui\.set_town_background' = 'self.background_manager.set_town_background'
    'self\.gui\.set_shop_background' = 'self.background_manager.set_shop_background'
    'self\.gui\.set_blacksmith_background' = 'self.background_manager.set_blacksmith_background'
    'self\.gui\.set_tavern_background' = 'self.background_manager.set_tavern_background'
    'self\.gui\.reset_background' = 'self.background_manager.reset_background'
    'self\.gui\.current_biome' = 'self.background_manager.current_biome'
    'self\.gui\.main_menu' = 'self.navigation.main_menu'
    'self\.gui\.combat' = 'self.combat'
    'self\.gui\.shop' = 'self.shop'
    'self\.gui\.blacksmith' = 'self.blacksmith'
    'self\.gui\.inventory' = 'self.inventory'
    'self\.gui\.tavern' = 'self.tavern'
    'self\.gui\.town' = 'self.town'
    'self\.gui\.quest_manager' = 'self.quest_manager'
    'self\.gui\.save_load_manager' = 'self.save_load_manager'
    'self\.gui\.monster_encounter' = 'self.monster_encounter'
    'self\.gui\.achievements' = 'self.achievements'
}

foreach ($file in $files) {
    Write-Host "Processing $file..." -ForegroundColor Cyan
    
    $content = Get-Content $file -Raw
    
    foreach ($pattern in $replacements.Keys) {
        $replacement = $replacements[$pattern]
        $content = $content -replace $pattern, $replacement
    }
    
    Set-Content -Path "$file.refactored" -Value $content
    Write-Host "  Created $file.refactored" -ForegroundColor Green
}

Write-Host "`nRefactoring complete! Review .refactored files before replacing originals." -ForegroundColor Yellow
