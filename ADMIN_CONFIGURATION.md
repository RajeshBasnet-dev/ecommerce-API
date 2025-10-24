# Django E-commerce Admin Configuration

This document provides an overview of the Django admin configuration for the E-commerce platform, detailing how each model is managed through the admin interface.

## Overview

The admin interface has been configured to provide comprehensive management capabilities for all models in the e-commerce platform. Each model has been customized with appropriate display options, filters, search capabilities, and actions.

## Model Configurations

### Accounts

#### User Model
- **Display Fields**: Username, Email, Role, Staff Status, Active Status, Date Joined
- **Filters**: Role, Staff Status, Active Status, Date Joined
- **Search**: Username, Email, First Name, Last Name
- **Read-only**: Date Joined, Last Login
- **Actions**: Standard Django user actions

#### BlacklistedToken Model
- **Display Fields**: JTI, User, Expiration Date, Created Date
- **Filters**: Expiration Date, Created Date
- **Search**: JTI, User Username, User Email
- **Read-only**: Created Date

### Products

#### Category Model
- **Display Fields**: Name, Product Count, Created Date, Updated Date
- **Search**: Name, Description
- **Read-only**: Created Date, Updated Date
- **Ordering**: By Name

#### Product Model
- **Display Fields**: Title, Seller, Category, Price, Stock, Active Status, Created Date
- **Filters**: Category, Active Status, Created Date, Seller
- **Search**: Title, Description, Seller Store Name, Category Name
- **Read-only**: Created Date, Updated Date
- **Editable Fields**: Active Status, Stock
- **Actions**: 
  - Mark as Active
  - Mark as Inactive
  - Restock Products (+100 units)

### Orders

#### Order Model
- **Display Fields**: ID, User, Status, Total Price, Created Date, Shipped Date, Delivered Date
- **Filters**: Status, Created Date, Shipped Date, Delivered Date, User
- **Search**: User Username, User Email, Order ID
- **Read-only**: Created Date, Updated Date, Shipped Date, Delivered Date, Total Price
- **Inline**: Order Items
- **Actions**:
  - Mark as Shipped
  - Mark as Delivered
  - Mark as Cancelled

#### OrderItem Model
- **Display Fields**: Order, Product, Quantity, Price, Total Price
- **Filters**: Order Status, Order Created Date
- **Search**: Order ID, Product Title
- **Read-only**: Order, Product, Quantity, Price, Total Price

### Cart

#### Cart Model
- **Display Fields**: User, Item Count, Created Date, Updated Date
- **Search**: User Username, User Email
- **Read-only**: Created Date, Updated Date
- **Inline**: Cart Items

#### CartItem Model
- **Display Fields**: Cart, Product, Quantity, Added Date, Total Price
- **Filters**: Added Date, Cart User
- **Search**: Cart User Username, Product Title
- **Read-only**: Added Date, Total Price

### Reviews

#### Review Model
- **Display Fields**: User, Product, Rating, Created Date, Updated Date
- **Filters**: Rating, Created Date, Updated Date, Product Category
- **Search**: User Username, User Email, Product Title, Comment
- **Read-only**: Created Date, Updated Date

### Payments

#### Payout Model
- **Display Fields**: Seller, Amount, Status, Transaction ID, Created Date, Processed Date
- **Filters**: Status, Created Date, Processed Date, Seller
- **Search**: Seller Store Name, Transaction ID
- **Read-only**: Created Date, Processed Date
- **Actions**:
  - Mark as Completed
  - Mark as Failed

### Sellers

#### SellerProfile Model
- **Display Fields**: User, Store Name, Verification Status, Earnings, Created Date, Updated Date
- **Filters**: Verification Status, Created Date, Updated Date
- **Search**: User Username, User Email, Store Name
- **Read-only**: Earnings, Created Date, Updated Date
- **Actions**:
  - Verify Sellers
  - Unverify Sellers

### Messages

#### Message Model
- **Display Fields**: Sender, Receiver, Order, Read Status, Created Date
- **Filters**: Read Status, Created Date, Sender, Receiver
- **Search**: Sender Username, Receiver Username, Order ID
- **Read-only**: Created Date, Updated Date
- **Actions**:
  - Mark as Read
  - Mark as Unread

### Analytics

#### SalesAnalytics Model
- **Display Fields**: Date, Total Sales, Total Orders, Total Products Sold, Created Date
- **Filters**: Date, Created Date
- **Search**: Date
- **Read-only**: Created Date
- **Ordering**: By Date (Descending)

#### UserActivity Model
- **Display Fields**: User, Activity Type, Product, Timestamp
- **Filters**: Activity Type, Timestamp, User
- **Search**: User Username, User Email, Activity Type, Product Title
- **Read-only**: Timestamp

## Security Features

1. **Staff-only Access**: All admin interfaces are restricted to staff users only
2. **Read-only Sensitive Data**: Timestamps and computed fields are marked as read-only
3. **Field-level Permissions**: Sensitive fields like earnings are read-only
4. **Search Restrictions**: Search is limited to non-sensitive fields

## Custom Actions

The admin interface includes several custom actions for bulk operations:

- **Order Management**: Mark orders as shipped, delivered, or cancelled
- **Product Management**: Activate/inactivate products, restock inventory
- **Seller Management**: Verify/unverify sellers
- **Payment Management**: Mark payouts as completed or failed
- **Message Management**: Mark messages as read/unread

## Performance Optimizations

- **Pagination**: All list views use pagination (25 items per page)
- **Indexing**: Models are ordered by relevant fields for performance
- **Selective Fields**: Only necessary fields are displayed to reduce database queries

## Usage Instructions

1. Access the admin interface at `/admin/`
2. Log in with staff credentials
3. Navigate to the desired model section
4. Use filters and search to find specific records
5. Select records and use actions for bulk operations
6. Edit individual records as needed

This configuration provides a comprehensive and user-friendly interface for managing all aspects of the e-commerce platform.