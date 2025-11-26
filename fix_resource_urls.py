"""
Script to fix or remove invalid resource URLs (like example.com)
"""

from app import app, db, LearningResource

def fix_resource_urls():
    """Remove or update resources with invalid example.com URLs"""
    with app.app_context():
        # Find resources with example.com URLs
        invalid_resources = LearningResource.query.filter(
            LearningResource.url.like('%example.com%')
        ).all()
        
        if invalid_resources:
            print(f"Found {len(invalid_resources)} resources with example.com URLs")
            for resource in invalid_resources:
                print(f"  - {resource.title}: {resource.url}")
                # Delete these invalid resources
                db.session.delete(resource)
            
            db.session.commit()
            print(f"✅ Removed {len(invalid_resources)} invalid resources")
        else:
            print("✅ No invalid resources found")
        
        # Count remaining resources
        total = LearningResource.query.count()
        print(f"\n📊 Total valid resources: {total}")

if __name__ == '__main__':
    print("=" * 70)
    print("Fixing Resource URLs")
    print("=" * 70)
    fix_resource_urls()
    print("=" * 70)
    print("✅ Done!")

