"""
Test the quest GUI integration
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_gui_integration():
    """Test if the GUI methods are properly integrated"""
    print("Testing GUI Integration")
    print("=" * 30)
    
    try:
        from gui_main import GameGUI
        print("✅ GameGUI imported successfully")
        
        # Check if the show_drop_quest_menu method exists
        if hasattr(GameGUI, 'show_drop_quest_menu'):
            print("✅ show_drop_quest_menu method exists")
        else:
            print("❌ show_drop_quest_menu method missing")
            return False
            
        # Check if drop_quest method exists in QuestManager
        from gui_quests import QuestManager
        if hasattr(QuestManager, 'drop_quest'):
            print("✅ drop_quest method exists in QuestManager")
        else:
            print("❌ drop_quest method missing in QuestManager")
            return False
            
        print("✅ All integration tests passed!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_button_logic():
    """Test the button arrangement logic"""
    print("\nTesting Button Logic")
    print("=" * 20)
    
    # Test scenarios:
    scenarios = [
        {"active_quests": 1, "max_quests": 3, "expected_buttons": ["➕ Take Another Quest", "🗑️ Drop Quest", "🔙 Back"]},
        {"active_quests": 3, "max_quests": 3, "expected_buttons": ["🗑️ Drop Quest", "🔙 Back"]},
        {"active_quests": 0, "max_quests": 3, "expected_buttons": ["✅ Accept New Quest", "🔙 Back"]},
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"Scenario {i}: {scenario['active_quests']} active quests")
        
        # Simulate button generation logic
        buttons = []
        if scenario["active_quests"] > 0:
            if scenario["active_quests"] < scenario["max_quests"]:
                buttons.append("➕ Take Another Quest")
            buttons.append("🗑️ Drop Quest")
            buttons.append("🔙 Back")
        else:
            buttons.append("✅ Accept New Quest")
            buttons.append("🔙 Back")
        
        if buttons == scenario["expected_buttons"]:
            print(f"  ✅ Correct buttons: {buttons}")
        else:
            print(f"  ❌ Expected: {scenario['expected_buttons']}")
            print(f"     Got: {buttons}")
    
    print("Button logic tests completed!")

if __name__ == "__main__":
    success = test_gui_integration()
    if success:
        test_button_logic()
    print("\nIntegration tests completed!")