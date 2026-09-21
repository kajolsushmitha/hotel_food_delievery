import re
from typing import Optional, List, Dict, Any
from backend.repository.hotel_repository import (
    get_hotel_by_id,
    get_hotel_by_name,
    get_all_hotels,
    get_active_hotels_with_menus
)
from backend.repository.menu_repository import (
    get_menu_items_by_hotel
)
from backend.repository.history_repository import (
    get_hotel_revenue_summary,
    get_all_hotels_revenue_summary
)
from backend.chatbot.ollama_service import ask_llama


def extract_hotel_mention_from_text(message: str, existing_hotels: List[Dict[str, Any]]) -> Optional[str]:
   
    msg_lower = message.strip().lower()

    # Generic hotel/restaurant queries should not be matched as a single hotel name
    generic_inquiries = [
        "what are the hotel available",
        "what are the hotels available",
        "which hotels are available",
        "which restaurants are available",
        "what restaurants are available",
        "available hotels",
        "available restaurants",
        "list hotels",
        "list restaurants",
        "all hotels",
        "all restaurants",
        "show hotels",
        "show restaurants",
        "highest revenue",
        "lowest revenue",
        "total revenue of all",
        "all revenue"
    ]
    for generic in generic_inquiries:
        if generic in msg_lower:
            return None

    # 1. Match against known hotel names in DB (case-insensitive)
    for hotel in existing_hotels:
        hotel_name = hotel["name"].lower()
        # Word boundary match to avoid partial substrings
        if re.search(rf'\b{re.escape(hotel_name)}\b', msg_lower):
            return hotel["name"]

    # 2. Extract potential restaurant names from patterns like "for Annapoorna", "in KFC", "from KFC", "at KFC"
    patterns = [
        r'\bfor\s+(?:the\s+)?([a-zA-Z0-9\s\'\-_]+?)(?:\?|\.|\!|\,|$|\s+menu|\s+food|\s+hotel|\s+restaurant)',
        r'\bin\s+([a-zA-Z0-9\s\'\-_]+?)(?:\?|\.|\!|\,|$|\s+menu|\s+food|\s+hotel|\s+restaurant)',
        r'\bat\s+([a-zA-Z0-9\s\'\-_]+?)(?:\?|\.|\!|\,|$|\s+menu|\s+food|\s+hotel|\s+restaurant)',
        r'\bfrom\s+([a-zA-Z0-9\s\'\-_]+?)(?:\?|\.|\!|\,|$|\s+menu|\s+food|\s+hotel|\s+restaurant)'
    ]
    for pattern in patterns:
        match = re.search(pattern, message, re.IGNORECASE)
        if match:
            candidate = match.group(1).strip()
            # Ignore common stopwords or generic terms
            if candidate.lower() not in {"the", "a", "an", "this", "our", "all", "your", "hotel", "hotels", "restaurant", "restaurants", "highest", "lowest", "total"}:
                return candidate

    return None


def chat_with_hotel_menu(
    message: str,
    hotel_id: Optional[int] = None,
    hotel_name: Optional[str] = None
) -> str:
    """
    Dynamically answers user questions about menus, hotels, and order revenue based on real database records.
    """
    msg_lower = message.strip().lower()
    is_revenue_query = any(
        kw in msg_lower for kw in [
            "revenue", "sales", "earned", "earning", "earnings", "income",
            "highest", "lowest", "most order", "how many order", "order count",
            "hotel_order_history", "history", "turnover"
        ]
    )

    
    if hotel_id is not None:
        hotel = get_hotel_by_id(hotel_id)
        if not hotel or not hotel.get("is_active", True):
            return f"Hotel with ID {hotel_id} was not found or is currently inactive in our database."
        
        if is_revenue_query:
            rev_summary = get_hotel_revenue_summary(hotel_id)
            db_context = (
                f"HOTEL / RESTAURANT: {hotel['name']} (Location: {hotel['location']})\n"
                f"HISTORICAL ORDERS & REVENUE (from hotel_order_history table):\n"
                f"- Total Orders Completed: {rev_summary['total_orders']}\n"
                f"- Total Historical Revenue: Rs. {rev_summary['total_revenue']:.2f}"
            )
        else:
            menu_items = get_menu_items_by_hotel(hotel_id)
            available_items = [item for item in menu_items if item.get("is_available")]
            menu_text = "\n".join(
                f"- {item['name']} | Rs. {item['price']} | Category: {item['category']}" + (f" | {item['description']}" if item.get('description') else "")
                for item in available_items
            ) if available_items else "No menu items available."

            db_context = (
                f"HOTEL / RESTAURANT: {hotel['name']} (Location: {hotel['location']})\n\n"
                f"AVAILABLE MENU:\n{menu_text}"
            )

    # 2. If hotel_name is specified
    elif hotel_name is not None and hotel_name.strip():
        hotel = get_hotel_by_name(hotel_name.strip())
        if not hotel or not hotel.get("is_active", True):
            all_hotels = get_all_hotels()
            active_names = [h["name"] for h in all_hotels if h.get("is_active", True)]
            hotels_list_str = ", ".join(active_names) if active_names else "None"
            return (
                f"Sorry, '{hotel_name}' is not found in our database. "
                f"Available hotels/restaurants in our system are: {hotels_list_str}."
            )

        if is_revenue_query:
            rev_summary = get_hotel_revenue_summary(hotel["id"])
            db_context = (
                f"HOTEL / RESTAURANT: {hotel['name']} (Location: {hotel['location']})\n"
                f"HISTORICAL ORDERS & REVENUE (from hotel_order_history table):\n"
                f"- Total Orders Completed: {rev_summary['total_orders']}\n"
                f"- Total Historical Revenue: Rs. {rev_summary['total_revenue']:.2f}"
            )
        else:
            menu_items = get_menu_items_by_hotel(hotel["id"])
            available_items = [item for item in menu_items if item.get("is_available")]
            menu_text = "\n".join(
                f"- {item['name']} | Rs. {item['price']} | Category: {item['category']}" + (f" | {item['description']}" if item.get('description') else "")
                for item in available_items
            ) if available_items else "No menu items available."

            db_context = (
                f"HOTEL / RESTAURANT: {hotel['name']} (Location: {hotel['location']})\n\n"
                f"AVAILABLE MENU:\n{menu_text}"
            )

    # 3. Dynamic lookup from user message
    else:
        all_hotels = get_all_hotels()
        active_hotels = [h for h in all_hotels if h.get("is_active", True)]

        if not active_hotels:
            return "There are currently no active hotels or restaurants in our database."

        mentioned_hotel_str = extract_hotel_mention_from_text(message, active_hotels)

        if mentioned_hotel_str:
            matched_hotel = get_hotel_by_name(mentioned_hotel_str)
            if matched_hotel and matched_hotel.get("is_active", True):
                if is_revenue_query:
                    rev_summary = get_hotel_revenue_summary(matched_hotel["id"])
                    db_context = (
                        f"HOTEL / RESTAURANT: {matched_hotel['name']} (Location: {matched_hotel['location']})\n"
                        f"HISTORICAL ORDERS & REVENUE (from hotel_order_history table):\n"
                        f"- Total Orders Completed: {rev_summary['total_orders']}\n"
                        f"- Total Historical Revenue: Rs. {rev_summary['total_revenue']:.2f}"
                    )
                else:
                    menu_items = get_menu_items_by_hotel(matched_hotel["id"])
                    available_items = [item for item in menu_items if item.get("is_available")]
                    menu_text = "\n".join(
                        f"- {item['name']} | Rs. {item['price']} | Category: {item['category']}" + (f" | {item['description']}" if item.get('description') else "")
                        for item in available_items
                    ) if available_items else "No menu items available."

                    db_context = (
                        f"HOTEL / RESTAURANT: {matched_hotel['name']} (Location: {matched_hotel['location']})\n\n"
                        f"AVAILABLE MENU:\n{menu_text}"
                    )
            else:
                active_names = [h["name"] for h in active_hotels]
                hotels_list_str = ", ".join(active_names)
                return (
                    f"Sorry, '{mentioned_hotel_str}' is not available in our database. "
                    f"Available hotels/restaurants are: {hotels_list_str}."
                )
        else:
            if is_revenue_query or "what are the hotel" in msg_lower or "list hotels" in msg_lower:
                revenue_list = get_all_hotels_revenue_summary()
                hotel_loc_map = {h["id"]: h.get("location", "") for h in active_hotels}
                # Revenue & Hotel catalog summary sorted by revenue
                hotel_list_overview = "\n".join(
                    f"- {r['hotel_name']} (Location: {hotel_loc_map.get(r['hotelId'], '')}) | Total Orders: {r['total_orders']} | Total Revenue: Rs. {r['total_revenue']:.2f}"
                    for r in revenue_list
                )
                db_context = (
                    f"HOTELS / RESTAURANTS & REVENUE (from hotel_order_history, sorted highest to lowest):\n{hotel_list_overview}"
                )
            else:
                records = get_active_hotels_with_menus()
                hotels_dict = {}
                for r in records:
                    hid = r["hotel_id"]
                    h_name = r["hotel_name"]
                    if hid not in hotels_dict:
                        hotels_dict[hid] = {
                            "name": h_name,
                            "location": r["hotel_location"],
                            "items": []
                        }
                    if r["item_name"]:
                        hotels_dict[hid]["items"].append(
                            f"- {r['item_name']} (Rs. {r['price']}, {r['category']})"
                        )

                hotel_list_overview = "\n".join(
                    f"{i+1}. {h['name']} (Location: {h['location']})"
                    for i, h in enumerate(active_hotels)
                )

                context_lines = []
                for hid, data in hotels_dict.items():
                    items_str = "\n  ".join(data["items"]) if data["items"] else "  No menu items listed."
                    context_lines.append(f"HOTEL / RESTAURANT: {data['name']} (Location: {data['location']})\n  {items_str}")

                db_context = (
                    f"REGISTERED HOTELS / RESTAURANTS LIST:\n{hotel_list_overview}\n\n"
                    f"AVAILABLE MENUS:\n" + "\n\n".join(context_lines)
                )

    # Construct strict database-grounded prompt for Llama
    prompt = f"""You are a helpful food ordering and restaurant assistant for our multi-restaurant food delivery system.

DATABASE RECORDS:
\"\"\"
{db_context}
\"\"\"

USER QUESTION:
\"{message}\"

STRICT INSTRUCTIONS:
1. When the user asks for a menu or available food items:
   - List ONLY the menu items from 'AVAILABLE MENU' with their name, price, and category.
   - Do NOT include or mention total orders, order count, sales, or total revenue.
   - Group the items neatly by category (e.g. Breakfast, Starters, Main Course, Beverages, Pizza) if multiple categories exist.
2. REVENUE / SALES INSTRUCTION: When asked about revenue, sales, earnings, or orders for any hotel, use ONLY the official total revenue and order count given under 'HISTORICAL ORDERS & REVENUE'.
3. HOTELS LIST INSTRUCTION: If asked what hotels or restaurants are available, list the registered hotels/restaurants with their locations.
4. Answer strictly using ONLY the database records provided above. Do not invent any numbers, food items, or hotels.
5. Keep the response clean, direct, polite, and well-formatted.
"""

    try:
        return ask_llama(prompt)
    except Exception as e:
        return f"Database query succeeded, but AI assistant error occurred: {str(e)}"