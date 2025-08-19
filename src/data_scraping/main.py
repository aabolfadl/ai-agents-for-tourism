#!/usr/bin/env python3
"""
Egyptian Monuments Web Scraper
Main script with command-line interface for scraping museums, archaeological sites, and sunken monuments.
"""

import sys
import argparse
from scraper import EgyptMonumentsScraper
from config import BASE_URLS, OUTPUT_FILES, CHECKPOINT_FILES


def create_scraper(site_type: str) -> EgyptMonumentsScraper:
    """Create a scraper instance for the specified site type."""
    if site_type not in BASE_URLS:
        raise ValueError(f"Invalid site type: {site_type}. Available types: {list(BASE_URLS.keys())}")
    
    return EgyptMonumentsScraper(
        site_type=site_type,
        base_url=BASE_URLS[site_type],
        checkpoint_file=CHECKPOINT_FILES[site_type],
        output_file=OUTPUT_FILES[site_type]
    )


def scrape_single_type(site_type: str) -> None:
    """Scrape a single site type."""
    try:
        scraper = create_scraper(site_type)
        scraper.scrape_all()
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print(f"\nScraping of {site_type} interrupted by user.")
    except Exception as e:
        print(f"Unexpected error while scraping {site_type}: {e}")
        sys.exit(1)


def scrape_all_types() -> None:
    """Scrape all available site types."""
    for site_type in BASE_URLS.keys():
        print(f"\n{'='*50}")
        print(f"Starting scrape of {site_type.upper()}")
        print(f"{'='*50}")
        
        try:
            scraper = create_scraper(site_type)
            scraper.scrape_all()
        except KeyboardInterrupt:
            print(f"\nScraping interrupted. You can resume later by running the script again.")
            break
        except Exception as e:
            print(f"Error scraping {site_type}: {e}")
            continue
    
    print(f"\n{'='*50}")
    print("All scraping tasks completed!")
    print(f"{'='*50}")


def show_statistics() -> None:
    """Show statistics for all site types."""
    print("\nScraping Statistics:")
    print("=" * 60)
    
    for site_type in BASE_URLS.keys():
        try:
            scraper = create_scraper(site_type)
            stats = scraper.get_statistics()
            
            print(f"\n{site_type.upper()}:")
            print(f"  Total entries: {stats['total_entries']}")
            print(f"  With services: {stats['entries_with_services']}")
            print(f"  With hours: {stats['entries_with_hours']}")
            print(f"  With prices: {stats['entries_with_prices']}")
            
        except Exception as e:
            print(f"\n{site_type.upper()}: Error loading data - {e}")


def main():
    """Main entry point with argument parsing."""
    parser = argparse.ArgumentParser(
        description="Scrape Egyptian monuments data from egymonuments.gov.eg",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --type museums                    # Scrape only museums
  python main.py --type archaeological-sites      # Scrape only archaeological sites  
  python main.py --type sunken-monuments          # Scrape only sunken monuments
  python main.py --all                            # Scrape all types
  python main.py --stats                          # Show statistics
        """
    )
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--type", 
        choices=list(BASE_URLS.keys()),
        help="Type of site to scrape"
    )
    group.add_argument(
        "--all", 
        action="store_true",
        help="Scrape all site types"
    )
    group.add_argument(
        "--stats", 
        action="store_true",
        help="Show scraping statistics"
    )
    
    parser.add_argument(
        "--list-types",
        action="store_true", 
        help="List available site types"
    )
    
    args = parser.parse_args()
    
    if args.list_types:
        print("Available site types:")
        for site_type, url in BASE_URLS.items():
            print(f"  {site_type}: {url}")
        return
    
    if args.stats:
        show_statistics()
    elif args.all:
        scrape_all_types()
    elif args.type:
        scrape_single_type(args.type)


if __name__ == "__main__":
    main()