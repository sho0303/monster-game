"""
Blacksmith system for GUI - provides services instead of selling items
"""
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gui_interfaces import GameContextProtocol


class BlacksmithGUI:
    """Blacksmith service system for GUI"""
    def __init__(self, gui: 'GameContextProtocol'):
        """Initialize with game context.
        
        Args:
            gui: Game context providing UI, state, and subsystem access
        """
        self.gui = gui
        self.services = {
            'Sharpen Sword': {
                'name': 'Sharpen Sword',
                'cost': 100,
                'description': 'Permanently adds +1 damage to your weapon',
                'stat': 'attack',
                'bonus': 1,
                'icon': '⚔️',
                'message': 'Your weapon gleams with deadly sharpness!'
            },
            'Bolster Armour': {
                'name': 'Bolster Armour', 
                'cost': 100,
                'description': 'Permanently adds +1 defense to your armor',
                'stat': 'defense',
                'bonus': 1,
                'icon': '🛡️',
                'message': 'Your armor is reinforced with expert craftsmanship!'
            }
        }
    
    def open(self):
        """Open blacksmith shop"""
        # Set the blacksmith-specific background
        self.gui.set_blacksmith_background()
        
        self.gui.clear_text()
        self.gui.lock_interface()
        
        # Show blacksmith intro
        self.gui.print_text("⚒️  IRONFORGE BLACKSMITH  ⚒️")
        self.gui.print_text("=" * 60)
        self.gui.print_text("\nThe burly blacksmith wipes sweat from his brow")
        self.gui.print_text("as he looks up from the glowing forge.")
        self.gui.print_text("\n\"Greetings, adventurer! I can enhance your gear")
        self.gui.print_text("with the finest craftsmanship in the realm.\"")
        
        # Display gold with colored value
        gold_amount = self.gui.game_state.hero.get('gold', 0)
        self.gui.print_text("")
        self.gui.print_colored_value("💰 Your Gold: ", gold_amount, 'gold')
        self.gui.print_text("")
        
        self._show_services()
    
    def _show_services(self):
        """Display available blacksmith services"""
        self.gui.print_text("=" * 60)
        self.gui.print_text("BLACKSMITH SERVICES:")
        self.gui.print_text("=" * 60)
        
        # Show each service
        services_list = list(self.services.values())
        for i, service in enumerate(services_list, 1):
            self.gui.print_text(f"\n{i}. {service['icon']} {service['name']} - 💰 {service['cost']} gold")
            self.gui.print_text(f"   📋 {service['description']}")
        
        self.gui.print_text("\n" + "=" * 60)
        self.gui.print_text("\"Choose a service, and I'll get to work immediately!\"")
        
        # Set buttons for service interaction
        def on_service_action(choice):
            if choice <= len(services_list):
                selected_service = services_list[choice - 1]
                self._purchase_service(selected_service)
            elif choice == len(services_list) + 1:
                # Return to town
                self._leave_blacksmith()
        
        # Set button labels
        button_labels = []
        for service in services_list:
            button_labels.append(f"{service['icon']} {service['name']}")
        button_labels.append("🚪 Leave Blacksmith")
        
        self.gui.set_buttons(button_labels, on_service_action)
        self.gui.unlock_interface()
    
    def _purchase_service(self, service):
        """Handle service purchase"""
        # Lock interface to prevent double-purchases
        self.gui.lock_interface()
        
        hero = self.gui.game_state.hero
        service_cost = service['cost']
        hero_gold = hero.get('gold', 0)
        
        # Check if hero has enough gold
        if hero_gold < service_cost:
            self.gui.clear_text()
            self.gui.print_text(f"\n❌ Not enough gold for {service['name']}!")
            self.gui.print_text(f"   You have: 💰 {hero_gold}")
            self.gui.print_text(f"   You need: 💰 {service_cost}")
            self.gui.print_text(f"   Short by: 💰 {service_cost - hero_gold}")
            
            self.gui.print_text(f"\nThe blacksmith shakes his head sadly.")
            self.gui.print_text(f"\"Come back when you have more coin, friend.\"")
            
            # Return to services menu after delay
            self.gui.root.after(3000, lambda: [self.gui.clear_text(), self._show_services()])
            return
        
        # Deduct gold
        hero['gold'] -= service_cost
        
        # Apply service effect
        stat_name = service['stat']
        bonus = service['bonus']
        old_value = hero.get(stat_name, 0)
        hero[stat_name] += bonus
        new_value = hero[stat_name]
        
        # Show dramatic blacksmith work sequence
        self._show_blacksmith_work(service, old_value, new_value)
    
    def _show_blacksmith_work(self, service, old_value, new_value):
        """Show animated blacksmith working on the enhancement"""
        self.gui.clear_text()
        
        # Work sequence
        work_messages = [
            f"The blacksmith takes your {service['name'].lower().split()[1]} and examines it carefully...",
            f"He heats the forge to blazing temperatures! 🔥",
            f"*CLANG* *CLANG* *CLANG*",
            f"Sparks fly as hammer strikes metal! ✨⚒️✨", 
            f"The blacksmith quenches the hot metal! 💨",
            f"He polishes and sharpens with expert precision...",
            f"\"There! Perfect craftsmanship!\" 👨‍🔧"
        ]
        
        def show_work_step(step=0):
            if step < len(work_messages):
                if step == 0:
                    self.gui.clear_text()
                    self.gui.print_text("⚒️  ENHANCEMENT IN PROGRESS  ⚒️")
                    self.gui.print_text("=" * 60)
                
                self.gui.print_text(f"\n{work_messages[step]}")
                
                # Continue to next step after delay
                delay = 1500 if step in [2, 3] else 1000  # Longer delay for dramatic effect
                self.gui.root.after(delay, lambda: show_work_step(step + 1))
            else:
                # Show final result
                self._show_enhancement_result(service, old_value, new_value)
        
        # Start the work sequence
        show_work_step()
    
    def _show_enhancement_result(self, service, old_value, new_value):
        """Show the final enhancement result"""
        self.gui.clear_text()
        
        self.gui.print_text("✅  ENHANCEMENT COMPLETE!  ✅")
        self.gui.print_text("=" * 60)
        
        # Show success message with colored service name
        success_parts = [
            (f"\n{service['icon']} Service completed: ", "#00ff00"),
            (service['name'], "#ffaa00"),
            ("!", "#00ff00")
        ]
        self.gui._print_colored_parts(success_parts)
        
        # Show stat improvement
        stat_parts = [
            (f"\n📊 {service['stat'].title()}: ", "#ffffff"),
            (str(old_value), "#ff6666"),
            (" → ", "#ffffff"),
            (str(new_value), "#00ff00"),
            (f" (+{service['bonus']})", "#ffdd00")
        ]
        self.gui._print_colored_parts(stat_parts)
        
        # Show enhancement message
        self.gui.print_text(f"\n✨ {service['message']}")
        
        # Gold remaining with colored amount
        hero_gold = self.gui.game_state.hero.get('gold', 0)
        self.gui.print_text("")
        self.gui.print_colored_value("💰 Gold remaining: ", hero_gold, 'gold')
        
        self.gui.print_text("\nThe blacksmith grins proudly at his work.")
        self.gui.print_text("\"That should serve you well in battle!\"")
        
        def continue_action():
            self.gui.clear_text()
            self._show_services()
        
        # Return to services menu after delay
        self.gui.root.after(4000, continue_action)
    
    def _leave_blacksmith(self):
        """Leave blacksmith and return to town"""
        self.gui.clear_text()
        self.gui.lock_interface()
        
        self.gui.print_text("🚪 Leaving the blacksmith...")
        self.gui.print_text("\"Farewell, adventurer! Come back anytime")
        self.gui.print_text("you need quality craftsmanship!\"")
        self.gui.print_text("\nYou step back into the town square.")
        
        # Return to town after delay
        self.gui.root.after(2000, self.gui.town.enter_town)
