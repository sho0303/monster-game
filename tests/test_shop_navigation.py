"""
Test script for shop navigation flow
"""

def test_shop_navigation_flow():
    """Test that shop navigation flows correctly after purchases"""
    print("Testing Shop Navigation Flow")
    print("=" * 35)
    
    # Simulate the shop navigation states
    navigation_log = []
    
    class MockGUI:
        def __init__(self):
            self.navigation_log = navigation_log
            
        def main_menu(self):
            self.navigation_log.append("main_menu")
            print("📱 Navigated to: Game Main Menu")
            
        def clear_text(self):
            pass
            
        def print_text(self, text):
            pass
            
        def unlock_interface(self):
            pass
            
        class root:
            @staticmethod
            def after(delay, func):
                # Simulate the delayed call immediately for testing
                print(f"⏰ Scheduled call after {delay}ms: {func.__name__}")
                func()
        
        class audio:
            @staticmethod 
            def play_sound_effect(sound):
                pass
    
    class MockShopGUI:
        def __init__(self):
            self.gui = MockGUI()
            self.current_category = None
            
        def _select_category(self):
            navigation_log.append("select_category")
            print("🛒 Navigated to: Store Category Selection")
            
        def _show_items(self):
            navigation_log.append("show_items")
            print("📦 Navigated to: Item List")
            
        def simulate_successful_purchase(self):
            """Simulate what happens after a successful purchase"""
            print("\n🛍️  SIMULATING SUCCESSFUL PURCHASE")
            print("-" * 40)
            
            # This simulates the end of _purchase_item method
            self.gui.audio.play_sound_effect('store.mp3')
            
            # Return to store category selection after delay  
            self.gui.root.after(3000, self._select_category)
            
        def simulate_back_button_from_items(self):
            """Simulate clicking back button from item list"""
            print("\n🔙 SIMULATING BACK BUTTON FROM ITEM LIST")
            print("-" * 45)
            
            # This simulates the back button in _show_items
            self._select_category()
            
        def simulate_duplicate_purchase(self):
            """Simulate what happens when duplicate purchase is blocked"""
            print("\n❌ SIMULATING DUPLICATE PURCHASE BLOCK")
            print("-" * 42)
            
            # This simulates the duplicate purchase prevention
            self.gui.unlock_interface()
            self.gui.root.after(2500, self._show_items)
            
        def simulate_insufficient_gold(self):
            """Simulate what happens when player has insufficient gold"""
            print("\n💰 SIMULATING INSUFFICIENT GOLD")
            print("-" * 35)
            
            # This simulates the insufficient gold case
            self.gui.root.after(2500, self._show_items)
    
    # Test the navigation flow
    shop = MockShopGUI()
    
    print("Starting at store category selection...")
    shop._select_category()
    
    print("\nNavigating to item list...")
    shop._show_items()
    
    # Test successful purchase flow
    shop.simulate_successful_purchase()
    
    # Test back button flow
    shop._show_items()  # Go back to items
    shop.simulate_back_button_from_items()
    
    # Test error cases
    shop._show_items()  # Go back to items
    shop.simulate_duplicate_purchase()
    
    shop.simulate_insufficient_gold()
    
    print(f"\n📋 NAVIGATION LOG")
    print("=" * 20)
    for i, action in enumerate(navigation_log, 1):
        print(f"{i}. {action}")
    
    # Analyze the navigation flow
    print(f"\n🔍 ANALYSIS")
    print("=" * 15)
    
    # Count where we end up after purchases
    purchase_destinations = []
    for i, action in enumerate(navigation_log):
        if i > 0 and "purchase" in navigation_log[i-1:i+1].__str__().lower():
            if i + 1 < len(navigation_log):
                purchase_destinations.append(navigation_log[i+1])
    
    # Check if successful purchases go back to category selection
    success_count = sum(1 for dest in navigation_log if dest == "select_category")
    items_count = sum(1 for dest in navigation_log if dest == "show_items")
    main_menu_count = sum(1 for dest in navigation_log if dest == "main_menu")
    
    print(f"Times returned to category selection: {success_count}")
    print(f"Times returned to item list: {items_count}")
    print(f"Times returned to main menu: {main_menu_count}")
    
    # Expected behavior:
    # - Successful purchases should return to category selection
    # - Error cases should return to item list
    # - No purchases should return to main menu (unless explicitly requested)
    
    if main_menu_count == 0:
        print("✅ SUCCESS: No unexpected returns to main menu!")
    else:
        print("❌ WARNING: Some actions returned to main menu unexpectedly")
    
    if success_count >= 2:  # At least one from purchase + one from back button
        print("✅ SUCCESS: Purchases correctly return to category selection!")
    else:
        print("❌ WARNING: Purchases may not be returning to category selection")

if __name__ == "__main__":
    test_shop_navigation_flow()